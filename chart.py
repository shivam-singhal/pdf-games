PDF_FILE_TEMPLATE = """
%PDF-1.6

1 0 obj
<<
  /AcroForm <<
    /Fields [ ###FIELD_LIST### ]
  >>
  /Pages <<
    /Count 1
    /Kids [ 16 0 R ]
    /Type /Pages
  >>
  /OpenAction 17 0 R
  /Type /Catalog
>>
endobj

21 0 obj
[
  ###FIELD_LIST###
]
endobj

###FIELDS###

16 0 obj
<<
  /Annots 21 0 R
  /Contents << >>
  /MediaBox [ 0 0 612 792 ]
  /Parent 7 0 R
  /Resources <<
    /Font <<
      /HeBo 10 0 R
    >>
  >>
  /Type /Page
>>
endobj

17 0 obj
<<
  /JS 42 0 R
  /S /JavaScript
>>
endobj

42 0 obj
<< >>
stream
console.println("Script loaded!");

function test_pattern() {
    console.println("Drawing test pattern");
    // Draw diagonal line
    for(var i = 0; i < 5; i++) {
        var field = this.getField(`P_${i}_${i}`);
        field.hidden = false;
        console.println(`Set pixel ${i},${i}`);
    }
}

endstream
endobj

trailer
<<
  /Root 1 0 R
>>
%%EOF
"""

PIXEL_OBJ = """
###IDX### obj
<<
  /FT /Btn
  /Ff 1
  /MK <<
    /BG [
      0.8
    ]
    /BC [
      0 0 0
    ]
  >>
  /Border [ 0 0 1 ]
  /P 16 0 R
  /Rect [
    ###RECT###
  ]
  /Subtype /Widget
  /T (P_###X###_###Y###)
  /Type /Annot
>>
endobj
"""

BUTTON_AP_STREAM = """
###IDX### obj
<<
  /BBox [ 0.0 0.0 ###WIDTH### ###HEIGHT### ]
  /FormType 1
  /Matrix [ 1.0 0.0 0.0 1.0 0.0 0.0]
  /Resources <<
    /Font <<
      /HeBo 10 0 R
    >>
    /ProcSet [ /PDF /Text ]
  >>
  /Subtype /Form
  /Type /XObject
>>
stream
q
0.75 g
0 0 ###WIDTH### ###HEIGHT### re
f
Q
q
1 1 ###WIDTH### ###HEIGHT### re
W
n
BT
/HeBo 12 Tf
0 g
10 8 Td
(###TEXT###) Tj
ET
Q
endstream
endobj
"""

BUTTON_OBJ = """
###IDX### obj
<<
  /A <<
    /JS ###SCRIPT_IDX### R
    /S /JavaScript
  >>
  /AP <<
    /N ###AP_IDX### R
  >>
  /F 4
  /FT /Btn
  /Ff 65536
  /MK <<
    /BG [
      0.75
    ]
    /CA (###LABEL###)
  >>
  /P 16 0 R
  /Rect [
    ###RECT###
  ]
  /Subtype /Widget
  /T (###NAME###)
  /Type /Annot
>>
endobj
"""

STREAM_OBJ = """
###IDX### obj
<< >>
stream
###CONTENT###
endstream
endobj
"""

# Configuration
GRID_SIZE = 5
PX_SIZE = 30
OFFSET_X = 200
OFFSET_Y = 400

fields_text = ""
field_indexes = []
obj_idx_ctr = 50

def add_field(field):
    global fields_text, field_indexes, obj_idx_ctr
    fields_text += field
    field_indexes.append(obj_idx_ctr)
    obj_idx_ctr += 1

def add_button(label, name, x, y, width, height, js):
    # Add JavaScript action
    script = STREAM_OBJ
    script = script.replace("###IDX###", f"{obj_idx_ctr} 0")
    script = script.replace("###CONTENT###", js)
    add_field(script)

    # Add button appearance
    ap_stream = BUTTON_AP_STREAM
    ap_stream = ap_stream.replace("###IDX###", f"{obj_idx_ctr} 0")
    ap_stream = ap_stream.replace("###TEXT###", label)
    ap_stream = ap_stream.replace("###WIDTH###", str(width))
    ap_stream = ap_stream.replace("###HEIGHT###", str(height))
    add_field(ap_stream)
    
    # Add button
    button = BUTTON_OBJ
    button = button.replace("###IDX###", f"{obj_idx_ctr} 0")
    button = button.replace("###SCRIPT_IDX###", f"{obj_idx_ctr-2} 0")
    button = button.replace("###AP_IDX###", f"{obj_idx_ctr-1} 0")
    button = button.replace("###LABEL###", label)
    button = button.replace("###NAME###", name)
    button = button.replace("###RECT###", f"{x} {y} {x + width} {y + height}")
    add_field(button)

print("Creating 5x5 test grid...")

# Create pixel grid
for x in range(GRID_SIZE):
    for y in range(GRID_SIZE):
        pixel = PIXEL_OBJ
        pixel = pixel.replace("###IDX###", f"{obj_idx_ctr} 0")
        pixel = pixel.replace("###RECT###", 
            f"{OFFSET_X+x*PX_SIZE} {OFFSET_Y+y*PX_SIZE} {OFFSET_X+x*PX_SIZE+PX_SIZE} {OFFSET_Y+y*PX_SIZE+PX_SIZE}")
        pixel = pixel.replace("###X###", f"{x}")
        pixel = pixel.replace("###Y###", f"{y}")
        add_field(pixel)

print("Adding button...")

# Add test button using the same method as Tetris
add_button("Test Pattern", "test_button", 
          OFFSET_X, OFFSET_Y - 40, 100, 30, 
          "test_pattern();")

print("Generating PDF...")

# Generate PDF
filled_pdf = PDF_FILE_TEMPLATE.replace("###FIELDS###", fields_text)
filled_pdf = filled_pdf.replace("###FIELD_LIST###", " ".join([f"{i} 0 R" for i in field_indexes]))

# Write to file in binary mode
print("Writing file...")
with open("test.pdf", "wb") as pdffile:
    pdffile.write(filled_pdf.encode('utf-8'))

print("Done! Open test.pdf - you should see a grid and a button that draws a pattern.")