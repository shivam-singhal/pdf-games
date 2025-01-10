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
// Game variables
var TICK_INTERVAL = 200;  // Slower game speed
var GRID_WIDTH = ###GRID_WIDTH###;
var GRID_HEIGHT = ###GRID_HEIGHT###;

var snake = [];
var direction = 'right';
var food = {x: 0, y: 0};
var score = 0;
var gameOver = false;
var interval = 0;

// Initialize pixel field references
var pixel_fields = [];

function init_pixels() {
    console.println("Initializing pixels...");
    for (var x = 0; x < GRID_WIDTH; ++x) {
        pixel_fields[x] = [];
        for (var y = 0; y < GRID_HEIGHT; ++y) {
            pixel_fields[x][y] = this.getField(`P_${x}_${y}`);
        }
    }
    console.println("Pixels initialized");
}

function spawn_food() {
    do {
        food.x = Math.floor(Math.random() * GRID_WIDTH);
        food.y = Math.floor(Math.random() * GRID_HEIGHT);
    } while (is_snake_at(food.x, food.y));
    console.println("Food spawned at: " + food.x + "," + food.y);
}

function is_snake_at(x, y) {
    return snake.some(segment => segment.x === x && segment.y === y);
}

function init_game() {
    console.println("Game initializing...");
    // Initialize snake in the middle
    snake = [{
        x: Math.floor(GRID_WIDTH / 2),
        y: Math.floor(GRID_HEIGHT / 2)
    }];
    direction = 'right';
    score = 0;
    gameOver = false;
    
    spawn_food();
    
    // Start game loop
    interval = app.setInterval("game_tick()", TICK_INTERVAL);
    
    // Update UI
    this.getField("T_score").value = "Score: 0";
    this.getField("B_start").hidden = true;
    console.println("Game initialized!");
}

function handle_input(event) {
    console.println("Input received: " + event.change);
    var newDir = direction;
    switch(event.change.toLowerCase()) {
        case 'w': newDir = 'up'; break;
        case 's': newDir = 'down'; break;
        case 'a': newDir = 'left'; break;
        case 'd': newDir = 'right'; break;
    }
    
    // Prevent 180-degree turns
    if ((direction === 'up' && newDir === 'down') ||
        (direction === 'down' && newDir === 'up') ||
        (direction === 'left' && newDir === 'right') ||
        (direction === 'right' && newDir === 'left')) {
        return;
    }
    
    direction = newDir;
    console.println("New direction: " + direction);
}

function move_snake() {
    var head = {x: snake[0].x, y: snake[0].y};
    
    switch(direction) {
        case 'up': head.y -= 1; break;
        case 'down': head.y += 1; break;
        case 'left': head.x -= 1; break;
        case 'right': head.x += 1; break;
    }
    
    // Check wall collision
    if (head.x < 0 || head.x >= GRID_WIDTH || 
        head.y < 0 || head.y >= GRID_HEIGHT) {
        game_over();
        return;
    }
    
    // Check self collision
    if (is_snake_at(head.x, head.y)) {
        game_over();
        return;
    }
    
    // Move snake
    snake.unshift(head);
    
    // Check food collision
    if (head.x === food.x && head.y === food.y) {
        score += 10;
        this.getField("T_score").value = `Score: ${score}`;
        spawn_food();
    } else {
        snake.pop();
    }
}

function game_over() {
    gameOver = true;
    app.clearInterval(interval);
    console.println("Game Over! Score: " + score);
    app.alert(`Game Over! Score: ${score}\nRefresh to restart.`);
}

function set_pixel(x, y, state) {
    if (x < 0 || y < 0 || x >= GRID_WIDTH || y >= GRID_HEIGHT) return;
    pixel_fields[x][GRID_HEIGHT - 1 - y].hidden = !state;
}

function draw() {
    // Clear screen
    for (var x = 0; x < GRID_WIDTH; ++x) {
        for (var y = 0; y < GRID_HEIGHT; ++y) {
            set_pixel(x, y, false);
        }
    }
    
    // Draw snake
    snake.forEach(segment => {
        set_pixel(segment.x, segment.y, true);
    });
    
    // Draw food
    set_pixel(food.x, food.y, true);
}

function game_tick() {
    if (!gameOver) {
        move_snake();
        draw();
    }
}

// Initialize pixel references
console.println("Starting initialization...");
init_pixels();
console.println("Initialization complete!");

// Zoom to fit
app.execMenuItem("FitPage");

endstream
endobj

trailer
<<
  /Root 1 0 R
>>
%%EOF
"""

BUTTON_AP_STREAM = """
###IDX### obj
<<
  /BBox [ 0.0 0.0 ###WIDTH### ###HEIGHT### ]
  /FormType 1
  /Matrix [ 1.0 0.0 0.0 1.0 0.0 0.0 ]
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
0.8 0.8 0.8 rg
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

PIXEL_OBJ = """
###IDX### obj
<<
  /FT /Btn
  /Ff 1
  /MK <<
    /BG [ ###COLOR### ]
    /BC [ 0 0 0 ]
  >>
  /F 4
  /Border [ 0 0 1 ]
  /P 16 0 R
  /Rect [ ###RECT### ]
  /Subtype /Widget
  /T (P_###X###_###Y###)
  /Type /Annot
>>
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
    /BG [ 0.8 0.8 0.8 ]
    /BC [ 0 0 0 ]
  >>
  /P 16 0 R
  /Rect [ ###RECT### ]
  /Subtype /Widget
  /T (###NAME###)
  /Type /Annot
>>
endobj
"""

TEXT_OBJ = """
###IDX### obj
<<
    /AA <<
        /K <<
            /JS ###SCRIPT_IDX### R
            /S /JavaScript
        >>
    >>
    /F 4
    /FT /Tx
    /MK <<
        /BG [ 1 1 1 ]
        /BC [ 0 0 0 ]
    >>
    /P 16 0 R
    /Rect [ ###RECT### ]
    /Subtype /Widget
    /T (###NAME###)
    /Type /Annot
    /V (###LABEL###)
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

# Game configuration
PX_SIZE = 20
GRID_WIDTH = 15
GRID_HEIGHT = 15
GRID_OFF_X = 200
GRID_OFF_Y = 350

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
    script = STREAM_OBJ.replace("###IDX###", f"{obj_idx_ctr} 0").replace("###CONTENT###", js)
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
    button = button.replace("###NAME###", name if name else f"B_{obj_idx_ctr}")
    button = button.replace("###RECT###", f"{x} {y} {x + width} {y + height}")
    add_field(button)

def add_text(label, name, x, y, width, height, js):
    script = STREAM_OBJ.replace("###IDX###", f"{obj_idx_ctr} 0").replace("###CONTENT###", js)
    add_field(script)
    
    text = TEXT_OBJ
    text = text.replace("###IDX###", f"{obj_idx_ctr} 0")
    text = text.replace("###SCRIPT_IDX###", f"{obj_idx_ctr-1} 0")
    text = text.replace("###LABEL###", label)
    text = text.replace("###NAME###", name)
    text = text.replace("###RECT###", f"{x} {y} {x + width} {y + height}")
    add_field(text)

# Add playing field border
border = PIXEL_OBJ
border = border.replace("###IDX###", f"{obj_idx_ctr} 0")
border = border.replace("###COLOR###", "0.7 0.7 0.7")  # Gray border
border = border.replace("###RECT###", 
    f"{GRID_OFF_X-2} {GRID_OFF_Y-2} {GRID_OFF_X+GRID_WIDTH*PX_SIZE+2} {GRID_OFF_Y+GRID_HEIGHT*PX_SIZE+2}")
border = border.replace("###X###", "border")
border = border.replace("###Y###", "border")
add_field(border)

# Create playing field pixels
for x in range(GRID_WIDTH):
    for y in range(GRID_HEIGHT):
        pixel = PIXEL_OBJ
        pixel = pixel.replace("###IDX###", f"{obj_idx_ctr} 0")
        pixel = pixel.replace("###COLOR###", "0 0 0")  # Black pixels
        pixel = pixel.replace("###RECT###", 
            f"{GRID_OFF_X+x*PX_SIZE} {GRID_OFF_Y+y*PX_SIZE} {GRID_OFF_X+x*PX_SIZE+PX_SIZE} {GRID_OFF_Y+y*PX_SIZE+PX_SIZE}")
        pixel = pixel.replace("###X###", f"{x}")
        pixel = pixel.replace("###Y###", f"{y}")
        add_field(pixel)

# Add controls
add_button("Start Game", "B_start", 
    GRID_OFF_X + (GRID_WIDTH*PX_SIZE)/2-50, 
    GRID_OFF_Y + (GRID_HEIGHT*PX_SIZE)/2-25, 
    100, 50, "init_game();")

add_text("Use WASD keys to control snake", "T_input", 
    GRID_OFF_X, GRID_OFF_Y - 50, 
    GRID_WIDTH*PX_SIZE, 30, "handle_input(event);")

add_text("Score: 0", "T_score", 
    GRID_OFF_X + GRID_WIDTH*PX_SIZE + 10, 
    GRID_OFF_Y + GRID_HEIGHT*PX_SIZE - 50, 
    100, 30, "")

# Generate final PDF
filled_pdf = PDF_FILE_TEMPLATE.replace("###FIELDS###", fields_text)
filled_pdf = filled_pdf.replace("###FIELD_LIST###", " ".join([f"{i} 0 R" for i in field_indexes]))
filled_pdf = filled_pdf.replace("###GRID_WIDTH###", f"{GRID_WIDTH}")
filled_pdf = filled_pdf.replace("###GRID_HEIGHT###", f"{GRID_HEIGHT}")

# Write to file
with open("snake.pdf", "w", encoding='utf-8') as pdffile:
    pdffile.write(filled_pdf)
