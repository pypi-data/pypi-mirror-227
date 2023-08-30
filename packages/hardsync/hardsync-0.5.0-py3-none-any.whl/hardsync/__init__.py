import os
from pathlib import Path

__version__ = "0.5.0"
__hash__ = "50be789b85c1c362a27b02206d3d74cf48ed779d"
root_dir = Path(os.path.dirname(os.path.abspath(__file__)))
cpp_src_dir = root_dir / 'cpp' / 'src'
test_data_dir = root_dir / 'tests' / 'test_data'

