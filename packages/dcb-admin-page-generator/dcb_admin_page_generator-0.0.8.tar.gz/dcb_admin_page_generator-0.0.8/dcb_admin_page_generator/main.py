import json
from .page_class import *
from .funcs import *


def generate_page_list(configuration, generator_title, file_path, generator_type):
    return GenerateList(configuration, generator_title, file_path, generator_type)


def generate_page_add(configuration, generator_title, file_path, generator_type):
    return GenerateAdd(configuration, generator_title, file_path, generator_type)


def generator(config, file_path):
    # page_type = input('请输入想要生成的Page Type(list,add,form,dialog_list,dialog_add,dialog_form)')
    # file_path = get_user_input('输入生成目标路径(不填生成在当前根页面)')
    file_path = file_path + "/" if file_path else ""
    generator_title = get_user_input('请输入生成页面标题(必填)')
    generator_type = get_user_input('请输入想要生成的Page Type(1、list 2、add 3、dialog_list 4、dialog_add 5、list_v2)')
    page_dict = {'1': 'list', 'list': 'list',
                 '2': 'add', 'add': 'add',
                 '3': 'dialog_list', 'dialog_list': 'dialog_list',
                 '4': 'dialog_add', 'dialog_add': 'dialog_add',
                 '5': 'list_v2', 'list_v2': 'list_v2',
                 }
    generator_type = page_dict[generator_type]
    if generator_type == 'list':
        return generate_page_list(config, generator_title, file_path, generator_type)
    elif generator_type == 'add':
        return generate_page_add(config, generator_title, file_path, generator_type)
    elif generator_type == 'dialog_list':
        return generate_page_list(config, generator_title, file_path, generator_type)
    elif generator_type == 'dialog_add':
        return generate_page_add(config, generator_title, file_path, generator_type)
    elif generator_type == 'list_v2':
        return generate_page_list(config, generator_title, file_path, generator_type)


# if __name__ == '__main__':
    # from config import defineConfig as temp_cfg
    # target_file_path = input('输入生成目标路径')
    # page_title = input('请输入生成页面标题')
    # page_type = input('请输入想要生成的Page Type(1、list 2、add 3、dialog_list 4、dialog_add)')
    # my_generator = generator(temp_cfg, page_title, page_type, '')
    # with open('res_text.vue', 'w', encoding='utf8') as f:
    #     f.write(my_generator.generate())

    # read_template(1)
