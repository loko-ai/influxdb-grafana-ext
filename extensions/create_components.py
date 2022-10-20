from loko_extensions.model.components import Component, Input, Output, save_extensions, Select, Arg, Dynamic, \
    MultiKeyValue, MKVField


component_description = ""
save_data_service = "save_data"
delete_data_service = ""
query_db_service = ""

################################# SAVE ARGS ##################################
save_group = "Save Parameters"
measurement_name = Arg(name="measurement_name", label="Measurement Name", type="text", group=save_group, required=True)

mkvfields_tags = [MKVField(name="tag_key", label="Tags Key")]
tags = MultiKeyValue(name="tags", label="Tags List", fields=mkvfields_tags, group=save_group)

mkvfields_fields = [MKVField(name="field_key", label="Field Key")]
fields = MultiKeyValue(name="fields", label="Fields List", fields=mkvfields_fields, group=save_group)


save_args = [measurement_name, tags, fields]
################################# Delete ARGS #################################
delete_group = "Delete Parameters"

delete_args = []
############################## QUERY ARGS ######################################
query_group = "Query Parameters"

query_args = []

############# ARGS
args_list = save_args + delete_args + query_args

###############################################################################
input_list = [Input(id="save", label="Save", to="save", service=save_data_service),
              Input(id="delete", label="Delete", to="save", service=save_data_service),
              Input(id="query", label="Query", to="save", service=save_data_service),
              ]
output_list = [Output(id="save", label="Save"), Output(id="delete", label="Delete"), Output(id="query", label="Query")]

influxDB_component = Component(name="InfluxDB", description=component_description, inputs=input_list, outputs=output_list, args=args_list,icon="RiStackFill" )

save_extensions([influxDB_component])
