import "@typespec/json-schema";
import "./metadata.tsp";

using TypeSpec.JsonSchema;

@jsonSchema("river")
@extension("additionalProperties", false)
model river {
  type: "river";
  metadata: {
    ...river_metadata;
    ...nztopo50_metadata;
  };
}

model river_metadata {}
