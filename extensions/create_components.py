from loko_extensions.model.components import Component, Input, Output, save_extensions, Select, Arg, Dynamic, \
    MultiKeyValue, MKVField


component_description = ""
save_data_service = "save_data"
delete_data_service = "delete_data"
query_db_service = "query"

################################# SAVE ARGS ##################################
save_group = "Save Parameters"
measurement_name = Arg(name="measurement_name", label="Measurement Name", type="text", group=save_group)

time_key = Arg(name="time", label="Time Key", type="text", group=save_group)



mkvfields_tags = [MKVField(name="tag_key", label="Tag Key")]
tags = MultiKeyValue(name="tags", label="Tags", fields=mkvfields_tags, group=save_group)

mkvfields_fields = [MKVField(name="field_key", label="Field Key")]
fields = MultiKeyValue(name="fields", label="Fields", fields=mkvfields_fields, group=save_group)


save_args = [measurement_name, time_key, tags, fields]
################################# Delete ARGS #################################
delete_group = "Delete Parameters"

measurement_del = Arg(name="measurement_delete", label="Measurement Name", type="text", group=delete_group)


start_del =  Arg(name="start_delete", label="Start", type="text", helper="Define the starting time to consider for deleting your data", group=delete_group, value="1970-01-01T00:00:00Z")
#helper= "Define the starting time to consider for deleting your data. The datetime format must be compatible with the one of your data",

stop_del = Arg(name="stop_delete", label="Stop", type="text", helper= "Define the stopping time to consider for deleting your data", group=delete_group)

delete_args = [measurement_del, start_del, stop_del]
############################## QUERY ARGS ######################################
query_group = "Query Parameters"

start_query = Arg(name="start_query", label="Start", type="text", helper="Define the starting time to consider for query your data", group=query_group, value="-50m")


query_args = [start_query]

############# ARGS
args_list = save_args + delete_args + query_args

###############################################################################
input_list = [Input(id="save", label="Save", to="save", service=save_data_service),
              Input(id="delete", label="Delete", to="save", service=delete_data_service),
              Input(id="query", label="Query", to="save", service=query_db_service),
              ]
output_list = [Output(id="save", label="Save"), Output(id="delete", label="Delete"), Output(id="query", label="Query")]

influxDB_component = Component(name="InfluxDB", description=component_description, inputs=input_list, outputs=output_list, args=args_list,icon="RiStackFill" )

save_extensions([influxDB_component])
