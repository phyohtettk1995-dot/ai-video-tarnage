# AI Video Dubbing App (Myanmar)

**ဘယ်လို Run မလဲ?**

၁။ **Folder တည်ဆောက်ပုံ အမှန်ဖြစ်ပါစေ:**
   - app.py
   - requirements.txt
   - templates/ (Folder)
       - index.html
   - static/ (Folder)
       - script.js

၂။ **Library များ Install လုပ်ရန်:**
   Terminal (သို့) Command Prompt ကိုဖွင့်ပြီး အောက်ပါစာကို ရိုက်ထည့်ပါ-
   `pip install -r requirements.txt`

၃။ **API Key ထည့်ရန်:**
   `app.py` ဖိုင်ထဲက `YOUR_GEMINI_API_KEY_HERE` ဆိုတဲ့ နေရာမှာ AI Studio ကနေ ယူထားတဲ့ သင်၏ Gemini API Key ကို အစားထိုးထည့်ပါ။

၄။ **Website ကို စတင် Run ရန်:**
   Terminal မှာ အောက်ပါစာကို ရိုက်ထည့်ပါ-
   `uvicorn app:app --reload`

၅။ **Website ကို ဖွင့်ရန်:**
   Browser တွင် `http://127.0.0.1:8000` ဟု ရိုက်ထည့်ပြီး အသုံးပြုနိုင်ပါပြီ!