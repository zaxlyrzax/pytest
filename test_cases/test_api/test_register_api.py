import pytest
import threading
from common.api_client import ApiClient
from common.assert_utils import successful_response,failed_response
from utils.file_reader import read_yaml
from conftest import logger
from common.db import get_user_byusername


class TestRegisterAPI:

    # 快乐路径：符合输入格式的用户名、密码、确认密码、邮箱、手机号
    # 关联登录业务
    @pytest.mark.api
    @pytest.mark.register
    @pytest.mark.positive
    @pytest.mark.parametrize('case',read_yaml('register_data.yaml',type="positive"))
    def test_register_positive(self,case,clean_user,register_api,user_api):
        username = case['username']
        response_register = register_api.register(case['username'],case['password'],
                                                  case['confirmPassword'],case['email'],case['phoneNumber'])
        print(f"response.json():{response_register.json()}")
        successful_response(response_register)
        logger.info(f"注册：{username}:{response_register.json().get('message')}")
        #数据库断言
        user = get_user_byusername(username)
        assert user is not None,f"注册接口返回成功，但数据库中添加{username}失败"
        assert user[0] == case['username'],f"数据库添加记录成功，但用户{username}写入错误"

        #注册好后，进行登录业务
        response_login = user_api.login(case['username'],case['password'])
        # 登录接口断言
        resp_json = successful_response(response_login)
        logger.info(f"登录：{username}:{resp_json.get('message')}")
        token = resp_json['data']['token']
        assert token is not None, "登录成功但未返回Token"
        assert len(token) > 10, "返回成功但长度异常"

        clean_user(username)

    # 异常测试：边界值、临界值、字符格式等
    @pytest.mark.api
    @pytest.mark.register
    @pytest.mark.negative
    @pytest.mark.parametrize('case',read_yaml("register_data.yaml",type="negative"))
    def test_register_negative(self, case,clean_user):
        username = case['username']

        client = ApiClient()

        response = client.post('/auth/register', json={
            "username":case['username'],
            "password":case['password'],
            "confirmPassword":case['confirmPassword'],
            "email":case['email'],
            "phoneNumber":case['phoneNumber'],
        })

        error_messages = []

        # ========== 断言1：接口返回校验 ==========
        try:
            assert failed_response(
                response,
                expected_code=case['expected_code'],
                expected_msg=case['expected_msg']
            )
        except AssertionError as e:
            error_messages.append(f"【接口断言失败】: {str(e)}")

        # ========== 断言2：数据库校验，负用例：不允许存在该用户 ==========
        try:
            if username != 'lisi':
                db_row = get_user_byusername(username)
                # 负向用例：数据库查询结果必须为None
                assert db_row is None, f"严重BUG：用户[{username}]接口返回失败，但已经非法写入数据库！"
        except AssertionError as e:
            error_messages.append(f"【数据库断言失败】: {str(e)}")

        # 登记用户名，session结束自动清理
        clean_user(username)

        logger.info(f"当前【测试场景】:{case['scenario']}")

        # 汇总所有错误，只要有任意一项失败，用例失败，打印全部错误信息
        if error_messages:
            err_text = "\n".join(error_messages)
            assert False, f"\n>>>>>>测试场景：{case['scenario']}\n{err_text}"

        logger.info(f"{case['scenario']} ---- passed")

    # 安全测试
    @pytest.mark.api
    @pytest.mark.register
    @pytest.mark.security
    @pytest.mark.parametrize('case',read_yaml("register_data.yaml", type="security"))
    def test_register_security(self,case,clean_user):
        username = case['username']

        client = ApiClient()
        response = client.post('/auth/register', json = {
            "username":case['username'],
            "password":case['password'],
            "confirmPassword": case['confirmPassword'],
            "email": case['email'],
            "phoneNumber": case['phoneNumber'],
        })

        error_messages = []

        # ========== 断言1：接口返回校验 ==========
        try:
            assert failed_response(
                response,
                expected_code=case['expected_code'],
                expected_msg=case['expected_msg']
            )
        except AssertionError as e:
            error_messages.append(f"【接口断言失败】: {str(e)}")

        # ========== 断言2：数据库校验，负用例：不允许存在该用户 ==========
        try:
            db_row = get_user_byusername(username)
            # 负向拦截用例：数据库一定不能查到这条记录
            assert db_row is None, f"安全漏洞：恶意payload【{username}】被存入数据库！"
        except AssertionError as e:
            error_messages.append(f"【数据库断言失败】: {str(e)}")

        # 登记用户名，session结束自动清理
        clean_user(username)

        logger.info(f"当前【测试场景】:{case['scenario']}")

        # 汇总所有错误，只要有任意一项失败，用例失败，打印全部错误信息
        if error_messages:
            err_text = "\n".join(error_messages)
            assert False, f"\n>>>>>>测试场景：{case['scenario']}\n{err_text}"

        logger.info(f"{case['scenario']} ---- passed")

    # 并发测试
    @pytest.mark.api
    @pytest.mark.register
    @pytest.mark.concurrent
    @pytest.mark.parametrize('case', read_yaml("register_data.yaml", type="concurrent"))
    def test_register_concurrent_click(self, case, clean_user):
        """
        模拟用户前端连续点击注册按钮，并发5次提交同一个注册表单
        预期：只有1次注册成功，其余请求应该返回用户名已存在；数据库不能出现多条同名用户
        """

        click_count = 5  # 模拟点击5次
        result_list = []
        thread_list = []
        username = case["username"]
        max_allow = case.get("allow_success_max", 1)
        # 启动5个线程并发请求
        for _ in range(click_count):
            t = threading.Thread(
                target=lambda c=case, res=result_list: res.append({
                    "response": ApiClient().post(
                        '/auth/register',
                        json={
                            "username": c['username'],
                            "password": c['password'],
                            "confirmPassword": c['confirmPassword'],
                            "email": c['email'],
                            "phoneNumber": c['phoneNumber'],
                        },
                        timeout=10
                    )
                })
            )
            thread_list.append(t)
            t.start()

        # 等待所有请求全部结束
        for t in thread_list:
            t.join()

        error_messages = []

        # 收集所有响应状态（不做严格全部成功，因为重复注册大部分应该报用户名已存在）
        success_count = 0
        for item in result_list:
            resp = item["response"]
            # 判断是否注册成功
            if resp.json().get("code") == case["expected_code"]:
                success_count += 1

        # 业务规则校验：同一个账号并发点击，**最多只能有1次注册成功**
        try:
            assert success_count <= max_allow, f"并发重复点击异常：成功注册次数{success_count}，最多允许{max_allow}次！"
        except AssertionError as e:
            error_messages.append(f"【接口校验异常】{str(e)}")

        # 数据库校验：数据库中该用户名只能有0或者1条记录，不能多条
        db_row = get_user_byusername(username)
        try:
            if success_count == 1:
                # 有一次成功，数据库必须存在该用户
                assert db_row is not None, "接口显示注册成功，数据库没有该用户！"
            else:
                # 全部失败，数据库不能存在用户
                assert db_row is None, "接口全部注册失败，但数据库已经生成用户！"
        except AssertionError as e:
            error_messages.append(f"【数据库校验异常】{str(e)}")

        # 清理测试用户
        clean_user(username)

        logger.info(f"【并发点击测试】场景:{case['scenario']},模拟点击次数:{click_count},成功次数:{success_count}")

        if error_messages:
            err_text = "\n".join(error_messages)
            assert False, f"\n>>>>>>测试场景：{case['scenario']}\n模拟点击次数:{click_count}\n{err_text}"

        logger.info(f"{case['scenario']} ---- passed")