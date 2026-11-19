import json
import unittest
from unittest.mock import MagicMock, patch

from tools.feasibility_probe import classify, parse_tensor_header, fetch


class FeasibilityTests(unittest.TestCase):
    def test_license(self):
        self.assertEqual(classify(["https://creativecommons.org/licenses/by/4.0/"]),
                         "candidate_explicit_by_or_cc0")
        self.assertEqual(classify(["https://creativecommons.org/licenses/by-nc/4.0/"]),
                         "restricted_nc_or_nd")
        self.assertEqual(classify(["openAccess"]), "unknown")

    def test_tensor_header(self):
        data = {"w": {"dtype": "BF16", "shape": [2, 3], "data_offsets": [0, 12]}}
        result = parse_tensor_header(json.dumps(data).encode())
        self.assertEqual(result["tensor_elements"], 6)
        self.assertEqual(result["payload_bytes_declared"], 12)

    def test_range_refuses_full_checkpoint(self):
        response = MagicMock()
        response.status = 200
        with patch("tools.feasibility_probe.urllib.request.urlopen") as open_url:
            open_url.return_value.__enter__.return_value = response
            with self.assertRaises(ValueError):
                fetch("https://example.org/model.safetensors", (0, 7))
        response.read.assert_not_called()


if __name__ == "__main__":
    unittest.main()
