from typing import Tuple, Any, List
from .plots.figure import Figure
import base64
import os
import re 
import pandas as pd
from salsa.parameters import Parameters
import plotly.graph_objects as go
import matplotlib.pyplot as plt
import socket
import pytz
from datetime import datetime

class Report:

    filepath: str
    
    def __init__(self, path):
        self.filepath = path
        self.tabsections: List[str] = []
        self.params = Parameters()
        return
    
    def __str__(self) -> str:
        result = "\t\t" + "="*10 + "\n"
        result += "\t\t" + "Report __str__():\n"
        result += "\t\t" + "This report's filepath: " + str(self.filepath) + "\n"
        result += "\t\t" + "This report's tabs: " + str(self.tabsections) + "\n\n"
        result += "\t\t" + "="*10 + "\n\n"
        return result


    def start_document(self, runID = ''):
        if runID == '':
             runID = self.params['runID']
        header = f"""<!DOCTYPE html>
<html>
<head>
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{runID} Report</title>
"""

        styling = """<style>
body {font-family: Arial;}

#sam-header {
  font-family: "Open Sans", verdana, arial, sans-serif;
}

/* Table styling */
#table-title {
  font-family: "Open Sans", verdana, arial, sans-serif;
  font-size: 16px;
  padding-left: 2em;
  color: #2a3f5f;
}

#rundmc-table {
  font-family: "Open Sans", verdana, arial, sans-serif;
  border-collapse: collapse;
}

#rundmc-table td, #rundmc-table th {
  border: 1px solid #ddd;
  padding: 4px;
  text-align: center;
  font-size: 14px;
}

#rundmc-table tr:nth-child(even){background-color: #ebf0f8;}

#rundmc-table tr:hover {background-color: #ddd;}

#rundmc-table th {
  padding-top: 8px;
  padding-bottom: 8px;
  background-color: #c8d4e3;
  color: #2a3f5f;
  font-weight: normal;
}

/* Style the tab */
.tab {
  overflow: hidden;
  border: 1px solid #ccc;
  background-color: #f1f1f1;
}

/* Style the buttons inside the tab */
.tab button {
  background-color: inherit;
  float: left;
  border: none;
  outline: none;
  cursor: pointer;
  padding: 14px 16px;
  transition: 0.3s;
  font-size: 17px;
}

/* Change background color of buttons on hover */
.tab button:hover {
  background-color: #ddd;
}

/* Create an active/current tablink class */
.tab button.active {
  background-color: #ccc;
}

/* Style the tab content */
.tabcontent {
  display: none;
  padding: 6px 12px;
  border: 1px solid #ccc;
  border-top: none;
}

.tabcontent {
  animation: fadeEffect 1s; /* Fading effect takes 1 second */
}

/* Go from zero to full opacity */
@keyframes fadeEffect {
  from {opacity: 0;}
  to {opacity: 1;}
}
/* Sticky div */
.sticky-div {
  background-color: white;
  position: sticky;
  top: 0px;
  padding: 10px 0px;
  z-index: 999;
}

 /* Collapsible tab */
.collapsible {
  background-color: #eee;
  cursor: pointer;
  padding: 18px;
  width: 100%;
  border: none;
  text-align: left;
  outline: none;
  font-size: 17px;
}

.collapsible:hover {
  background-color: #ddd;
}

.collapsible.active {
  background-color: #ccc
}

.run-details {
  padding: 0 18px;
  background-color: white;
  max-height: 0;
  overflow: hidden;
  transition: max-height 0.2s ease-out;
}

.collapsible:after {
  content: '\\02795'; /* Unicode character for "plus" sign (+) */
  font-size: 13px;
  color: white;
  float: right;
  margin-left: 5px;
}

.collapsible.active:after {
  content: "\\2796"; /* Unicode character for "minus" sign (-) */
}
</style>
</head>
<body style="background-color:white;">

<script>
function open_details() {
  var coll = document.getElementsByClassName("collapsible");
  var i;

  for (i = 0; i < coll.length; i++) {
    coll[i].classList.toggle("active");
    var content = coll[i].nextElementSibling;
    if (content.style.maxHeight){
      content.style.maxHeight = null;
    } else {
      content.style.maxHeight = content.scrollHeight + "px";
    }
  }
}

function openSection(evt, sectionName) {
  var i, tabcontent, tablinks;
  tabcontent = document.getElementsByClassName("tabcontent");
  for (i = 0; i < tabcontent.length; i++) {
    tabcontent[i].style.display = "none";
  }
  tablinks = document.getElementsByClassName("tablinks");
  for (i = 0; i < tablinks.length; i++) {
    tablinks[i].className = tablinks[i].className.replace(" active", "");
  }
  document.getElementById(sectionName).style.display = "block";
  evt.currentTarget.className += " active";
  
  document.body.scrollTop = 0;
  document.documentElement.scrollTop = 0;
}
</script>
"""
        with open(self.filepath, 'w+') as file:
                    file.write(header)
                    file.write(styling)
        return
    
    def add_sam_header(self, runID = '', version = '1.3.1.6', hostname = socket.gethostname(), timestamp = '', nexus_details = ''):
      if runID == '':
        runID = self.params['runID']
      if timestamp == '':
        timestamp = self.get_timestamp()

      # with open(self.paths['pipeline_version'], 'r') as file:
      #     text = file.read()
      # version = text.strip()

      header = f"""<div class="sticky-div" id="sam-header">
<h2>SAM Report - RunID{runID}</h2>
 <button type="button" class="collapsible" onclick="open_details()">Run Details</button>
<div class="run-details">
  <p><b>Generated with pipeline version {version} on server {hostname}</b></p>
  <p><b>{timestamp}</b></p>
  <p>Nexus details:<br>{nexus_details}</p>
</div> 
"""
      with open(self.filepath, 'a+') as file:
          file.write(header)
      return
    
    def set_tab_sections(self, names: List[str]):
      sections = """<div class="tab">\n"""
      self.tabsections = names
      for name in names:
        section = f'''<button class="tablinks" onclick="openSection(event, '{name} Section')" id="{"".join(name.split(' '))}">{name}</button>\n'''
        sections += section  
      sections += "</div>\n</div>\n"
      with open(self.filepath, 'a+') as file:
          file.write(sections)

    def add_section(self, section_name):
        new_section = f"""\n<div id="{section_name} Section" class="tabcontent">
</div>
"""
        with open(self.filepath, 'a+') as file:
            file.write(new_section)
        return
    
    def end_document(self):
        onstart = self.tabsections[0]
        footer = f"""
<script>
  document.getElementById("{onstart}").click();
</script>
</body>
</html>
        """
        with open(self.filepath, 'a+') as file:
                  file.write(footer)
        return
    

    def add_plot(self):
        return

    def seek_and_add(self, html: str):
        with open(self.filepath, 'r+') as file:
            file.seek(0, os.SEEK_END)
            eof = file.tell()
            file.seek(eof - 7)
            file.write(html + "\n</div>\n")
        return
    
    def add_table(self,  table: pd.DataFrame, title: str, **kwargs) -> None:
          default_kwargs = {"index": False,
                            "col_space":int(720/table.shape[1]),
                            "table_id":"rundmc-table",
                            "justify": "center"}
          default_kwargs.update(kwargs)
          table_html = table.to_html(**default_kwargs)
          html = f'<div>\n<p id="table-title">{title}</p>\n{table_html}\n<br>\n</div>'
          self.seek_and_add(html)
          return
    
    def add_to_html(self, fig: Figure):
        html = fig.to_html(full_html=False,
                            include_plotlyjs=False,
                            config = {'toImageButtonOptions': {'filename':re.sub("[ -]+", '_', fig.name)}})
        self.seek_and_add(html)
        return
    
    def save_png(self, fig, size: Tuple[Any, Any] = (None,None), newline: bool = True) -> None:
        base = self.params['save_loc']
        filename =  base + "temp_plot.png"
        
        # Check if fig is a Plotly figure
        if isinstance(fig, go.Figure):
            fig.write_image(filename)
        # Check if fig is a Matplotlib figure
        elif isinstance(fig, plt.Figure):
            fig.savefig(filename, format="png")
        else:
            raise ValueError("Unsupported figure type")
        
        self.add_png(filename, size, newline)
        os.remove(filename)
        return
    
    def add_png(self, png_path: str, size: Tuple[Any, Any] = (None,None), newline: bool = True) -> None:
        
        height = size[0]
        width = size[1]
        should_apply_size = ((height is not None) and (width is not None))
        
        png_base64 = base64.b64encode(open(png_path, 'rb').read()).decode('utf-8')
        img_tag_start = '<img'
        img_tag_file = f' alt="{png_path}" src="data:image/png;base64,{png_base64}"'
        img_tag_size = (should_apply_size)*f' height = "{height}" width = "{width}"'
        img_tag_end = f'>{newline*"<br>"}'
        
        img_tag = img_tag_start + img_tag_file + img_tag_size + img_tag_end
        self.seek_and_add(img_tag)
        return

    def get_timestamp(self):
        date_format='%Y %B %d - %H:%M %Z'
        date = datetime.now(tz=pytz.utc)
        #print 'Current date & time is:', date.strftime(date_format)
        
        date = date.astimezone(pytz.timezone('US/Pacific'))
        
        return date.strftime(date_format) 

    def start_tab(self, name: str):
        new_section = f"""\n<div id="{name} Section" class="tabcontent">
</div>
"""
        with open(self.filepath, 'a+') as file:
            file.write(new_section)
        return
      