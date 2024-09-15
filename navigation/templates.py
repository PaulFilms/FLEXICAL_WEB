import os
from menus import *
from db import *

# st.logo(os.path.join(path_resources, 'LOGO2.svg'))
st.title('TEMPLATES PAGE')

data = supabase.table('PROCEDURES').select('*').execute().data
print(data)

# Print results.
for row in data:
    st.write(row)
