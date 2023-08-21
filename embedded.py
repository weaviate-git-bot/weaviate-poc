import weaviate
import json

client = weaviate.Client(
    embedded_options=weaviate.embedded.EmbeddedOptions(),
)

uuid = client.data_object.create({
    'hello': 'World!'
}, 'MyClass')

obj = client.data_object.get_by_id(uuid, class_name='MyClass')

print(json.dumps(obj, indent=2))

if __name__ == '__main__':
    pass
