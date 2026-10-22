import "@typespec/json-schema";
import "./metadata.tsp";

using TypeSpec.JsonSchema;

@jsonSchema("ford")
@extension("additionalProperties", false)
model ford {
  type: "ford";
  metadata: {
    ...ford_metadata;
    ...nztopo50_metadata;
  };
}

model ford_metadata {
  /** Number of meteres to extend the blue road mask at the start of the road line */
  `nztopo50:ford:start_m`?: float64;

  /** Number of meters to extends the blue road mask at the end of the road line */
  `nztopo50:ford:end_m`?: float64;
}
