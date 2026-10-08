import os
import yaml

def read_yaml(file_name,**kwargs):
    #获取根目录路径
    base_dir = os.path.dirname(os.path.dirname(__file__))
    #拼接要读取的yaml文件路径
    file_path = os.path.join(base_dir,'data\\api',file_name)
    with open(file_path,'r',encoding='utf-8') as f:
        cases_data = yaml.safe_load(f)['cases_data']

        filter_type = kwargs.get("type")
        interfaceName = kwargs.get("interfaceName")

        if filter_type:
            if interfaceName:
                yaml_data = [case for case in cases_data if case.get('type') == filter_type and case.get('interfaceName') == interfaceName]
                return yaml_data
            else:
                yaml_data = [case for case in cases_data if case.get('type') == filter_type]
                return yaml_data
        else:
            yaml_data = cases_data
        return yaml_data


if __name__ == '__main__':
    for item in read_yaml('product_data.yaml',type='positive',interfaceName='createProduct'):
        if item['description']:
            print(item)
        else:
            pass