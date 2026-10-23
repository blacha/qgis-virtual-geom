model nztopo50_metadata {
  /** Hide the feature from rendering on the nztopo50 product */
  `nztopo50:visible`?: boolean;

  /** Override the geometry of the object when rendering the nztopo50 product (WKT string or hex-encoded WKB) */
  `nztopo50:geometry`?: string;
}

model nztopo250_metadata {
  /** Hide the feature from rendering on the nztopo50 product */
  `nztopo250:visible`?: boolean;

  /** Override the geometry of the object when rendering the nztopo50 product (WKT string or hex-encoded WKB) */
  `nztopo250:geometry`?: string;
}
