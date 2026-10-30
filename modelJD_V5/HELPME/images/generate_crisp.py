import subprocess

cmd = [
    r"C:\Program Files\Google\Chrome\Application\chrome.exe",
    "--headless",
    "--disable-gpu",
    "--force-device-scale-factor=2",
    r"--screenshot=C:\Users\ASUS\Documents\modelJD_V4\HELPME\images\figure_2_2_crisp_dm.png",
    "--window-size=1040,840",
    r"file:///C:/Users/ASUS/Documents/modelJD_V4/HELPME/images/figure_2_2_crisp_dm.html"
]

subprocess.run(cmd, check=True)
print("Rendered figure_2_2_crisp_dm.png successfully")
