import "@typespec/json-schema";
import "./metadata.tsp";

using TypeSpec.JsonSchema;

@jsonSchema("bridge")
@extension("additionalProperties", false)
model bridge {
  type: "bridge";
  metadata: {
    ...bridge_metadata;
    ...nztopo50_metadata;
    ...nztopo250_metadata;
  };
}

model bridge_metadata {
  /**
   * Suppress the left bridge symbol
   */
  `nztopo50:bridge:suppress_left`?: boolean;

  /**
   * Suppress the right bridge symbol
   */
  `nztopo50:bridge:suppress_right`?: boolean;

  /**
   * Suppress the start of the bridge symbol by X meters
   */
  `nztopo50:bridge:suppress_start_m`?: float64;

  /**
   * Suppress the end of the bridge symbol by X meters
   */
  `nztopo50:bridge:suppress_end_m`?: float64;
}
