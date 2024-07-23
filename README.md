# YNG Map Project

## Setup Instructions

### 1. Clone the repository

```bash
git clone https://github.com/yourusername/YNG_map_project.git
cd YNG_map_project
```

### 2. Create a virtual environment
Create a virtual environment to manage dependencies. You can use venv or any other virtual environment tool of your choice.

Using venv
```bash
python3 -m venv venv
```
### 3. Activate the virtual environment
On macOS and Linux
```bash
source venv/bin/activate
```
On Windows
```bash
venv\Scripts\activate
```
### 4. Install dependencies
Install the necessary dependencies using pip and the requirements.txt file.

```bash
pip install -r requirements.txt
```

### Generating Fake Data (Optional)
To generate fake data, run:

```bash
python generate_fake_data.py
```
This will generate a CSV file with fake member data and automatically geocode the data.

### 5. Run the project
To start the Streamlit app, run:

```bash
streamlit run runstreamlit.py
```
