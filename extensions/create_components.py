from loko_extensions.model.components import Component, Input, Output, save_extensions, Select, Arg, Dynamic, \
    MultiKeyValue, MKVField


component_description = ""
save_data_service = "save_data"
delete_data_service = "delete_data"
query_db_service = "query"
read_db_service = "read"

################################# SAVE ARGS ##################################
save_group = "Save Parameters"

bucket_save = Arg(name="bucket_save", label="Bucket Name", type="text", group=save_group, value='influx-bu')

manual = Arg(name="manual", label="Manual", type="boolean", group=save_group, value=True)

measurement_name = Dynamic(name="measurement_name", label="Measurement Name", parent='manual', condition='{parent}',
                           dynamicType="text", group=save_group)

time_key = Dynamic(name="time", label="Time Key", parent='manual', condition='{parent}', dynamicType="text",
                   group=save_group)

mkvfields_tags = [MKVField(name="tag_key", label="Tag Key")]
tags = Dynamic(name="tags", label="Tags", parent='manual', condition='{parent}', dynamicType='multiKeyValue',
               fields=mkvfields_tags, group=save_group)

mkvfields_fields = [MKVField(name="field_key", label="Field Key")]
fields = Dynamic(name="fields", label="Fields", parent='manual', condition='{parent}', dynamicType='multiKeyValue',
                 fields=mkvfields_fields, group=save_group)


save_args = [bucket_save, manual, measurement_name, time_key, tags, fields]

################################# Delete ARGS #################################
delete_group = "Delete Parameters"

bucket_del = Arg(name="bucket_del", label="Bucket Name", type="text", group=delete_group, value='influx-bu')

from_query_del = Arg(name='from_query_del', label='From query', type='boolean', group=delete_group, value=False)
measurement_del = Dynamic(name="measurement_delete", label="Measurement Name", parent='from_query_del',
                          dynamicType="text", condition='!{parent}', group=delete_group)


start_del = Arg(name="start_delete", label="Start", type="text",
                helper="Define the starting time to consider for deleting your data",
                group=delete_group, value="1970-01-01T00:00:00Z")

stop_del = Arg(name="stop_delete", label="Stop", type="text",
               helper= "Define the stopping time to consider for deleting your data",
               group=delete_group)

delete_args = [bucket_del, from_query_del, measurement_del, start_del, stop_del]

############################## READ ARGS ######################################
read_group = "Read Parameters"

bucket_read = Arg(name="bucket_read", label="Bucket Name", type="text", group=read_group, value='influx-bu')

measurement_read = Arg(name="measurement_read", label="Measurement Name", type="text", group=read_group)

start_read = Arg(name="start_read", label="Start", type="text",
                  helper="Define the starting time to consider for reading your data",
                  group=read_group,
                  value="1970-01-01T00:00:00Z")
stop_read = Arg(name="stop_read", label="Stop", type="text",
                  helper="Define the stopping time to consider for reading your data",
                  group=read_group)


read_args = [bucket_read, measurement_read, start_read, stop_read]

############# ARGS
args_list = save_args + delete_args + read_args

###############################################################################
input_list = [Input(id="save", label="Save", to="save", service=save_data_service),
              Input(id="read", label="Read", to="read", service=read_db_service),
              Input(id="delete", label="Delete", to="delete", service=delete_data_service),
              Input(id="query", label="Query", to="query", service=query_db_service),
              ]
output_list = [Output(id="save", label="Save"), Output(id="read", label="Read"), Output(id="delete", label="Delete"),
               Output(id="query", label="Query")]

influxDB_component = Component(name="InfluxDB", description=component_description, inputs=input_list,
                               outputs=output_list, args=args_list, icon="RiStackFill", group='Custom')

save_extensions([influxDB_component])
