import time, os
from tketool.mlsample.LocalSampleSource import LocalDisk_NLSampleSource
from tketool.JConfig import get_config_instance
from tketool.mlsample.NLSampleSource import NLSampleSourceBase
from tketool.mlsample.SampleSet import SampleSet
from prettytable import PrettyTable, ALL


def _truncate_content(content, max_length):
    return (content[:max_length] + '..') if len(content) > max_length else content


def set_list(path=None):
    """
    This function generates a PrettyTable list of sets from a specified source directory.
    path : The path to the source directory. If not specified, it is obtained from the config instance's 'sample_source_path'.
    """
    path = path if path else get_config_instance().get_config("sample_source_path")
    if not os.path.exists(path):
        raise Exception(f"can not find the path : {path}")

    source = LocalDisk_NLSampleSource(path)

    info_dict = source.get_dir_list()

    xtable = PrettyTable()
    # 设置表头
    xtable.field_names = ["Set name", "Count", "Columns", "description", "base_set"]

    for k in sorted(info_dict.keys()):
        v = info_dict[k]
        xtable.add_row([k, v['count'],
                        _truncate_content(str(v['meta']['label_keys']), 30),
                        _truncate_content(v['meta']['des'], 20),
                        _truncate_content(v['meta']['base_set'], 20)
                        ])

    print(xtable)


def set_info(setname, path=None):
    """
    This function prints out detailed information about a specific set.
    setname : The name of the specific set.
    path : The path to the source directory. If not specified, it is obtained from the config instance's 'sample_source_path'.
    """
    path = path if path else get_config_instance().get_config("sample_source_path")
    if not os.path.exists(path):
        raise Exception(f"can not find the path : {path}")
    source = LocalDisk_NLSampleSource(path)

    meta_data = source.get_metadata_keys(setname)

    print("basic info: \n")
    table = PrettyTable(header=False)
    table.hrules = ALL
    # 定义表格的列名
    table.field_names = ["Attribute", "Value"]
    # 添加数据
    table.add_row(["Name", setname])
    table.add_row(["Count", source.get_set_count(setname)])
    table.add_row(["base set", meta_data['base_set']])
    table.add_row(["keys", meta_data['label_keys']])
    table.add_row(["tags", meta_data['tags']])
    table.add_row(["des", meta_data['des']])
    print(table)
    print("Set file info:")
    source.print_set_info(setname)


def set_data_info(setname, label_key, path=None):
    """
    This function prints the count of  per label key.
    setname : The name of the specific set.
    label_key : Statistics the result will use the key
    path : The path to the source directory. If not specified, it is obtained from the config instance's 'sample_source_path'.
    """
    path = path if path else get_config_instance().get_config("sample_source_path")
    if not os.path.exists(path):
        raise Exception(f"can not find the path : {path}")
    source = LocalDisk_NLSampleSource(path)

    content_key = {}
    for item in SampleSet(source, setname):
        label_value = item[label_key]
        if label_value not in content_key:
            content_key[label_value] = 0
        content_key[label_value] += 1

    print("Data info (count of per label key): \n")
    table = PrettyTable(header=False)
    table.hrules = ALL
    # 定义表格的列名
    table.field_names = ["Attribute", "Value"]

    for k, v in content_key.items():
        table.add_row([k, v])

    print(table)


def delete_set(setname, path=None):
    """
    This function deletes a specific set from a specified source directory.
    setname : The name of the specific set to be deleted.
    path : The path to the source directory.
    """
    path = path if path else get_config_instance().get_config("sample_source_path")
    if not os.path.exists(path):
        raise Exception(f"can not find the path : {path}")
    source = LocalDisk_NLSampleSource(path)
    source.delete_set(setname)
    print(f"{setname} deleted.")


# def Info_of_set(sample_set: SampleSet, key_func):
#     key_dict = {}
#     for item in sample_set:
#         lable = key_func(item)
#         if lable not in key_dict:
#             key_dict[lable] = 0
#         key_dict[lable] += 1
#
#     # PRINT
#     print("\n 统计结果:")
#     for k, v in key_dict.items():
#         print(f"{k} : {v} \n")


def SplitSet(samplesource: NLSampleSourceBase, ori_set_name: str, key_func,
             name_to_key_dict: dict, need_shuffle=True):
    meta_data = samplesource.get_metadata_keys(ori_set_name)
    new_set_name_gen_list = []

    # Create new sample sets based on the provided name-to-key dictionary
    for n_setname in name_to_key_dict.keys():
        n_name = f"{ori_set_name}_{n_setname}"
        samplesource.create_new_set(n_name, f"split from {ori_set_name}", ["split"],
                                    meta_data['label_keys'], ori_set_name)
        new_set_name_gen_list.append(n_name)

    sample_set = SampleSet(samplesource, ori_set_name)
    if need_shuffle:
        sample_set = sample_set.shuffle()

    # Initialize a list of counters, each element is a dictionary to track the label count for a subset
    count_list = [{} for _ in name_to_key_dict.values()]

    for item in sample_set:
        cur_label = key_func(item)
        list_formattor = [item[key] for key in meta_data['label_keys']]
        # Find the appropriate subset
        for idx, subset_name in enumerate(name_to_key_dict.keys()):
            subset_dict = name_to_key_dict[subset_name]
            if cur_label in subset_dict and subset_dict[cur_label] > count_list[idx].get(cur_label, 0):
                samplesource.add_row(new_set_name_gen_list[idx], list_formattor)
                count_list[idx][cur_label] = count_list[idx].get(cur_label, 0) + 1
                break

    samplesource.flush()

# from tketool.mlsample.LocalSampleSource import LocalDisk_NLSampleSource
# path = "/Users/jiangke/Downloads/buffer2"
# # ldn = LocalDisk_NLSampleSource("/Users/jiangke/Downloads/buffer2")
# _print_set_details_info(path, "sectioncut-simple-nps_v10")
