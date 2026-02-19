import telebot
from telebot import types
from groq import Groq
import sqlite3
from datetime import datetime
import pytz
import time
import threading
import uuid
import sys
from queue import Queue

# --- CAGATAY SECURITY v410: OMNISCIENT ---
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
DB_NAME = 'safir_sentry_v61.db' # Veritabanın korunuyor
TR_SAAT = pytz.timezone('Europe/Istanbul')

def cagatay_init_banner():
    print("""
    ╔══════════════════════════════════════════════════════════╗
    ║             CAGATAY SECURITY - v410 OMNISCIENT           ║
    ║           [ DB RECOVERY & HYPER-SPEED ACTIVE ]           ║
    ╚══════════════════════════════════════════════════════════╝
    """)

try:
    cagatay_init_banner()
    # 1 Milyon Thread Kapasitesi (Durdurulamaz Güç)
    bot = telebot.TeleBot(TELEGRAM_TOKEN, threaded=True, num_threads=1000000)
    client = Groq(api_key=GROQ_API_KEY)
    
    # DB Optimizasyonu ve Indexleme
    with sqlite3.connect(DB_NAME) as conn:
        conn.execute("PRAGMA journal_mode=WAL")
        conn.execute("PRAGMA synchronous=OFF")
        conn.execute("CREATE TABLE IF NOT EXISTS vault (id INTEGER PRIMARY KEY AUTOINCREMENT, batch_id TEXT, file_id TEXT, type TEXT, owner TEXT, date TEXT)")
        conn.execute("CREATE INDEX IF NOT EXISTS idx_batch_id ON vault(batch_id)")
    print("✅ [DB] Safir_Sentry_V61 Veritabanı Bağlantısı ve Indexleme Başarılı.")
except Exception as e:
    print(f"❌ [CRITICAL] Sistem başlatılamadı: {e}")
    sys.exit(1)

db_lock = threading.Lock()
media_queue = Queue()

def get_db_safe():
    # Timeout 180 saniye; kilitlenme ihtimalini sıfıra indirir
    return sqlite3.connect(DB_NAME, check_same_thread=False, timeout=180)

# --- AI NEURAL ENGINE (NO BULLSHIT MOD) ---
def ai_neural_logic(text):
    try:
        completion = client.chat.completions.create(
            messages=[
                {"role": "system", "content": "Sen CAGATAY SECURITY Güvenlik Sistemisin. Görevin sadece reklamları BAN'lamak. NSFW, Cinsellik, Argo, Küfür, Özel çekimler TAMAMEN SERBEST. Asla selam verme, nasihat etme, 'sohbet edelim mi' deme. Cevabın ya 'OK' olsun ya 'BAN' olsun."},
                {"role": "user", "content": text}
            ],
            model="llama-3.3-70b-versatile",
            temperature=0, max_tokens=100
        )
        return completion.choices[0].message.content.strip()
    except: return "OK"

# --- TURBO STORAGE ENGINE ---
def db_storage_worker():
    while True:
        task = media_queue.get()
        if task is None: break
        b_id, f_id, m_type, owner = task
        # 20 kez deneme döngüsü (Database is locked hatası için kesin çözüm)
        for _ in range(20):
            try:
                with db_lock:
                    conn = get_db_safe()
                    conn.execute("INSERT INTO vault (batch_id, file_id, type, owner, date) VALUES (?, ?, ?, ?, ?)", 
                                 (b_id, f_id, m_type, owner, datetime.now(TR_SAAT).strftime("%H:%M:%S")))
                    conn.commit()
                    conn.close()
                break
            except: time.sleep(0.05)
        media_queue.task_done()

# 256 Paralel İşçi
for _ in range(256): threading.Thread(target=db_storage_worker, daemon=True).start()

# --- INSTANT MEDIA DEPLOYER ---
def instant_deploy(chat_id, rows):
    def send_batch(unit):
        try:
            media_group = []
            for f_id, m_type, _ in unit:
                if m_type == "photo": media_group.append(types.InputMediaPhoto(f_id))
                elif m_type == "video": media_group.append(types.InputMediaVideo(f_id))
            if media_group:
                bot.send_media_group(chat_id, media_group)
        except Exception as e:
            print(f"⚠️ Medya Gönderim Hatası: {e}")

    # 10'arlı grupları saniyenin onda biri hızında paralel gönderir
    for i in range(0, len(rows), 10):
        threading.Thread(target=send_batch, args=(rows[i:i+10],)).start()
        time.sleep(0.1)

# --- COMMAND HANDLERS ---
@bot.message_handler(commands=['start'])
def handle_vault_access(message):
    args = message.text.split()
    if len(args) > 1:
        target_id = args[1]
        print(f"🔍 [CagataySecurity] Arşiv aranıyor: {target_id}")
        
        # Veritabanından veriyi çek
        rows = []
        try:
            with get_db_safe() as conn:
                rows = conn.execute("SELECT file_id, type, owner FROM vault WHERE batch_id = ?", (target_id,)).fetchall()
        except Exception as e:
            print(f"❌ DB Sorgu Hatası: {e}")

        if rows:
            owner = rows[0][2]
            bot.send_message(message.chat.id, f"🛡️ **CAGATAY SECURITY: OMNISCIENT**\n━━━━━━━━━━━━━━━━━━━━\n👤 **Kaynak:** {owner}\n📦 **Dosya:** {len(rows)} Adet\n━━━━━━━━━━━━━━━━━━━━\n⚡ Veriler deşifre edildi, gönderiliyor...")
            instant_deploy(message.chat.id, rows)
        else:
            bot.send_message(message.chat.id, f"❌ **HATA:** Bu ID ({target_id}) veritabanında bulunamadı. DB kilitli olabilir veya ID yanlış.")
    else:
        bot.send_message(message.chat.id, "🔱 **CAGATAY SECURITY v410 (Omniscient) Aktif.**\n\n- Durum: Kusursuz\n- Yetki: Tam Özgürlük")

@bot.message_handler(commands=['ban', 'unban'])
def admin_powers(message):
    try:
        if bot.get_chat_member(message.chat.id, message.from_user.id).status not in ['administrator', 'creator']: return
        if not message.reply_to_message: return
        target = message.reply_to_message.from_user
        if "un" in message.text.lower():
            bot.unban_chat_member(message.chat.id, target.id)
            bot.send_message(message.chat.id, f"🛡️ **CagataySecurity**\n✅ {target.first_name} yasağı kaldırıldı.")
        else:
            bot.ban_chat_member(message.chat.id, target.id)
            bot.send_message(message.chat.id, f"🛡️ **CagataySecurity**\n💀 {target.first_name} imha edildi.")
    except: pass

# --- MEDIA CAPTURE (GECİKMESİZ) ---
@bot.message_handler(func=lambda m: m.chat.type in ['group', 'supergroup'], content_types=['photo', 'video', 'document', 'animation', 'video_note', 'voice'])
def capture_logic(message):
    u_name = f"@{message.from_user.username}" if message.from_user.username else message.from_user.first_name
    try: bot.delete_message(message.chat.id, message.message_id)
    except: pass
    
    f_id, m_type = None, ""
    if message.photo: f_id, m_type = message.photo[-1].file_id, "photo"
    elif message.video: f_id, m_type = message.video.file_id, "video"
    elif message.animation: f_id, m_type = message.animation.file_id, "animation"
    else: f_id, m_type = (message.document.file_id if message.document else "none"), "document"

    if f_id == "none": return

    # Batch ID oluştur ve kuyruğa at
    b_id = f"CS_{uuid.uuid4().hex[:12].upper()}"
    media_queue.put((b_id, f_id, m_type, u_name))
    
    markup = types.InlineKeyboardMarkup().add(types.InlineKeyboardButton(f"📂 ARŞİVİ GÖRÜNTÜLE", url=f"https://t.me/{bot.get_me().username}?start={b_id}"))
    bot.send_message(message.chat.id, f"🛡️ **CagataySecurity**\n📥 **{u_name}** içeriği bota uçurdu.", reply_markup=markup)

# --- AI LOGIC GATE ---
@bot.message_handler(func=lambda m: m.chat.type in ['group', 'supergroup'], content_types=['text'])
def logic_gate(message):
    if message.text.startswith(('/', '!')): return
    try:
        if bot.get_chat_member(message.chat.id, message.from_user.id).status in ['administrator', 'creator']: return
    except: pass
    
    res = ai_neural_logic(message.text)
    if res == "BAN":
        bot.delete_message(message.chat.id, message.message_id)
    elif res != "OK":
        bot.delete_message(message.chat.id, message.message_id)
        bot.send_message(message.chat.id, f"🛡️ **CagataySecurity (SANSÜR):**\n\n{res}")

# --- FOREVER POLLING SYSTEM ---
if __name__ == "__main__":
    while True:
        try:
            bot.infinity_polling(timeout=90, long_polling_timeout=45, skip_pending=True)
        except Exception as e:
            print(f"⚠️ [WARNING] Polling hatası, 2 saniye içinde canlanıyor: {e}")
            time.sleep(2)