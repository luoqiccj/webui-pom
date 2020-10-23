#coding=utf-8
import yaml
from utils.get_info import get_project_dir
from utils.get_info import log

class GetYamlData:
    def get_yaml_data(self,filename=None):
        if filename==None:
            filename = get_project_dir() + "\\YamlFile"+"\\test.yaml"
        log.info("filename=%s"% filename)
        fp = open(filename,encoding='utf-8')
        yaml_data = yaml.load(fp,Loader=yaml.FullLoader)
        log.info("yaml_data=%s"%yaml_data)
        log.info("yaml_data=%s" % yaml_data['test_env']['url'])

if __name__ == '__main__':
    yd = GetYamlData()
    yd.get_yaml_data()


