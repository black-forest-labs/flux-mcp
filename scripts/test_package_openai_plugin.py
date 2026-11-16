import unittest

from package_openai_plugin import mcp_submission_schema, schema_errors, server_errors


CORE_SCHEMA = {
    "$defs": {
        "streamableHttpServer": {
            "type": "object",
            "properties": {"type": {"const": "streamable-http"}, "url": {"type": "string"}},
            "required": ["type", "url"],
            "additionalProperties": False,
        }
    },
    "$ref": "#/$defs/streamableHttpServer",
}
DCR = {"com.openai": {"auth": {"type": "oauth", "client": {"mode": "dcr"}}}}


class SubmissionValidationTests(unittest.TestCase):
    def setUp(self):
        self.server = {"type": "streamable-http", "url": "https://mcp.bfl.ai/"}
        self.schema = mcp_submission_schema(CORE_SCHEMA)

    def test_approved_oauth_extension_is_valid(self):
        self.server["extensions"] = DCR
        self.assertEqual(schema_errors(self.server, self.schema), [])

    def test_generic_server_still_valid(self):
        self.assertEqual(schema_errors(self.server, self.schema), [])

    def test_does_not_modify_core_schema(self):
        self.assertNotIn("extensions", CORE_SCHEMA["$defs"]["streamableHttpServer"]["properties"])

    def test_unknown_fields_remain_invalid(self):
        self.server["urll"] = self.server["url"]
        self.assertTrue(schema_errors(self.server, self.schema))

    def test_unknown_extensions_and_auth_modes_remain_invalid(self):
        for extension in [{"unknown.vendor": {}}, {"com.openai": {"auth": {"type": "none"}}}]:
            with self.subTest(extension=extension):
                self.server["extensions"] = extension
                self.assertTrue(schema_errors(self.server, self.schema))

    def test_https_endpoint_with_or_without_slash(self):
        for url in ["https://mcp.bfl.ai/", "https://mcp.bfl.ai"]:
            self.assertEqual(server_errors({"mcpServers": {"bfl": {"url": url}}}), [])

    def test_http_endpoint_remains_invalid(self):
        self.assertTrue(server_errors({"mcpServers": {"bfl": {"url": "http://mcp.bfl.ai/"}}}))


if __name__ == "__main__":
    unittest.main()
