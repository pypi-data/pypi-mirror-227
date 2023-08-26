use crate::pipeline::{
    parser::expression_builders::ExpressionBuilder,
    transformation::{LookupTransformation, Transformation, JoinKind},
    PiperError, Schema, ValueType, pipelines::BuildContext,
};

use super::TransformationBuilder;

#[derive(Debug)]
pub struct LookupTransformationBuilder {
    join_kind: JoinKind,
    fields: Vec<(String, Option<String>, ValueType)>,
    source: String,
    key: Box<dyn ExpressionBuilder>,
}

impl LookupTransformationBuilder {
    pub fn new(
        join_kind: JoinKind,
        fields: Vec<(String, Option<String>, ValueType)>,
        source: String,
        key: Box<dyn ExpressionBuilder>,
    ) -> Box<Self> {
        Box::new(Self {
            join_kind,
            fields,
            source,
            key,
        })
    }
}

impl TransformationBuilder for LookupTransformationBuilder {
    fn build(&self, input_schema: &Schema, ctx: &BuildContext) -> Result<Box<dyn Transformation>, PiperError> {
        for f in self.fields.iter() {
            let name = f.1.as_ref().unwrap_or(&f.0);
            if input_schema.get_column_index(name).is_some() {
                return Err(PiperError::ColumnAlreadyExists(name.clone()));
            }
        }
        LookupTransformation::create(
            self.join_kind,
            input_schema,
            self.source.clone(),
            ctx.get_lookup_source(&self.source)?,
            self.fields.clone(),
            self.key.build(input_schema, ctx)?,
        ) as Result<Box<dyn Transformation>, PiperError>
    }
}
