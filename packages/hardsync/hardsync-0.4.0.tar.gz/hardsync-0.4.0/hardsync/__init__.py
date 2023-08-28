import os
from pathlib import Path

__version__ = "0.4.0"
__hash__ = "3181966a3add47944ad1245114c854190d3f6344"
root_dir = Path(os.path.dirname(os.path.abspath(__file__)))
cpp_src_dir = root_dir / 'cpp' / 'src'
test_data_dir = root_dir / 'tests' / 'test_data'

