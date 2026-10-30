import subprocess
from pathlib import Path

CHROME = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
IMAGES_DIR = Path(r"C:\Users\ASUS\Documents\modelJD_V4\HELPME\images")

figures = [
    ("figure_3_1_crisp_dm.html", "figure_3_1_crisp_dm.png", "1000,760"),
    ("figure_3_2_offline_training.html", "figure_3_2_offline_training.png", "1060,600"),
    ("figure_3_3_online_two_stage.html", "figure_3_3_online_two_stage.png", "1080,610"),
    ("figure_3_4_sequence_diagram.html", "figure_3_4_sequence_diagram.png", "1080,680"),
    ("figure_3_5_ui_recommendation.html", "figure_3_5_ui_recommendation.png", "1080,680"),
    ("figure_3_6_ui_catalog.html", "figure_3_6_ui_catalog.png", "1080,680"),
]

for html_name, png_name, win_size in figures:
    html_path = IMAGES_DIR / html_name
    png_path = IMAGES_DIR / png_name
    cmd = [
        CHROME,
        "--headless=new",
        "--disable-gpu",
        "--force-device-scale-factor=2",
        f"--screenshot={png_path}",
        f"--window-size={win_size}",
        f"file:///{html_path.as_posix()}"
    ]
    print(f"Rendering {png_name}...")
    res = subprocess.run(cmd, capture_output=True, text=True)
    if png_path.exists():
        print(f"  [OK] {png_name} created ({png_path.stat().st_size:,} bytes)")
    else:
        print(f"  [ERROR] {png_name} failed. Stderr: {res.stderr}")
