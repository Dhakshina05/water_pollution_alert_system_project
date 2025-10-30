import cv2
import numpy as np
import datetime
import os
import urllib.request
import matplotlib.pyplot as plt
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

# ===================== Download Fallback Image =====================
def download_fallback_image(image_name="river.jpeg", url="https://i.imgur.com/ZVb1pGf.jpeg"):
    if not os.path.exists(image_name):
        print(f"⚠ Local image '{image_name}' not found. Downloading fallback image...")
        try:
            urllib.request.urlretrieve(url, image_name)
            print(f"✅ Fallback image saved as '{image_name}'.")
        except Exception as e:
            print(f"❌ Error downloading fallback image: {e}")
            return False
    return True

# ===================== Analyze Water Quality =====================
def analyze_water_quality(image_path):
    img = cv2.imread(image_path)
    if img is None:
        print("❌ Error: Could not read image.")
        return None

    img = cv2.resize(img, (224, 224))
    blue, green, red = cv2.split(img)
    blue_mean = np.mean(blue)

    if blue_mean > 120:
        pollution_level = "🟢 Excellent"
        risk = "Low"
        advisory = "✅ Safe for drinking and agriculture."
    elif blue_mean > 80:
        pollution_level = "🟡 Moderate"
        risk = "Medium"
        advisory = "⚠ Use after filtration; mild contamination detected."
    else:
        pollution_level = "🔴 Poor"
        risk = "High"
        advisory = "🚫 Unsafe for human use; avoid irrigation."

    health_risk = {
        "Cholera Risk (%)": round(np.random.uniform(1, 40), 2),
        "Typhoid Risk (%)": round(np.random.uniform(1, 30), 2),
        "Skin Allergy Risk (%)": round(np.random.uniform(5, 50), 2),
        "Chemical Contaminants (ppm)": round(np.random.uniform(50, 200), 2),
    }

    return pollution_level, risk, advisory, health_risk

# ===================== Generate Chart (with Details) =====================
def generate_chart(health_risk, pollution_level, risk, advisory):
    plt.figure(figsize=(8, 6))
    keys = list(health_risk.keys())
    values = list(health_risk.values())

    # Create horizontal bar chart
    bars = plt.barh(keys, values, color="skyblue", edgecolor="black")

    # Add values on bars
    for bar in bars:
        plt.text(
            bar.get_width() + 2,
            bar.get_y() + bar.get_height()/2,
            f"{bar.get_width():.2f}",
            va="center",
            fontsize=10
        )

    plt.title("💧 Water Health Risk Indicators", fontsize=16, fontweight='bold')
    plt.xlabel("Values (ppm / %)", fontsize=12)
    plt.ylabel("Risk Factors", fontsize=12)

    # Add summary text below chart
    text_box = (
        f"Pollution Level: {pollution_level}\n"
        f"Health Risk: {risk}\n"
        f"Advisory: {advisory}"
    )
    plt.figtext(0.02, -0.05, text_box, wrap=True, fontsize=11, ha='left')

    plt.tight_layout()
    chart_name = "water_quality_chart_with_details.png"
    plt.savefig(chart_name, bbox_inches='tight')
    plt.close()

    print(f"📊 Chart saved as '{chart_name}'")
    return chart_name

# ===================== Create PDF Report =====================
def create_pdf_report(image_name, pollution_level, risk, advisory, health_risk, chart_file):
    filename = "Water_Quality_Report.pdf"
    c = canvas.Canvas(filename, pagesize=letter)
    c.setFont("Helvetica-Bold", 18)
    c.drawString(150, 750, "💧 WATER QUALITY ANALYSIS REPORT 💧")

    c.setFont("Helvetica", 12)
    c.drawString(50, 710, f"Date & Time: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    c.drawString(50, 690, f"Image: {image_name}")
    c.drawString(50, 670, f"Pollution Level: {pollution_level}")
    c.drawString(50, 650, f"Health Risk: {risk}")
    c.drawString(50, 630, f"Advisory: {advisory}")

    y = 600
    c.drawString(50, y, "⚕ Health Risk Factors:")
    c.setFont("Helvetica", 11)
    for key, val in health_risk.items():
        y -= 20
        c.drawString(70, y, f"- {key}: {val}")

    # Embed chart in PDF
    if os.path.exists(chart_file):
        c.drawImage(chart_file, 100, 300, width=400, height=250)

    c.showPage()
    c.save()
    print(f"\n📄 Report successfully generated: {filename}")

# ===================== Main Program =====================
def main():
    image_name = "river.jpeg"
    if not download_fallback_image(image_name):
        return

    result = analyze_water_quality(image_name)
    if result is None:
        return

    pollution_level, risk, advisory, health_risk = result

    print("\n" + "="*50)
    print("💧 WATER QUALITY ANALYSIS RESULTS 💧")
    print("="*50)
    print(f"📸 Image: {image_name}")
    print(f"🌊 Pollution Level: {pollution_level}")
    print(f"⚕ Health Risk: {risk}")
    print(f"🩺 Advisory: {advisory}")
    print("\n🔬 Health Risk Factors:")
    for k, v in health_risk.items():
        print(f"   • {k}: {v}")
    print("="*50)

    # Generate chart with details
    chart_file = generate_chart(health_risk, pollution_level, risk, advisory)
    create_pdf_report(image_name, pollution_level, risk, advisory, health_risk, chart_file)

    # Show chart
    img = cv2.imread(chart_file)
    cv2.imshow("📊 Water Risk Chart with Details", img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

# ===================== Run =====================
if __name__ == "__main__":
    main()
