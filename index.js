const { default: makeWASocket, useMultiFileAuthState, DisconnectReason } = require("@whiskeysockets/baileys");
const { Boom } = require("@hapi/boom");
const qrcode = require("qrcode-terminal");

async function connectToWhatsApp() {
    const { state, saveCreds } = await useMultiFileAuthState('auth_info');

    const sock = makeWASocket({
        auth: state,
        printQRInTerminal: true // Tani waxay QR Code ku dhex tusaysaa Terminal-ka
    });

    sock.ev.on('connection.update', (update) => {
        const { connection, lastDisconnect, qr } = update;
        if (qr) {
            qrcode.generate(qr, { small: true });
            console.log("Scan gareey QR Code-ka kore!");
        }
        if (connection === 'close') {
            const shouldReconnect = (lastDisconnect.error instanceof Boom)?.output?.statusCode !== DisconnectReason.loggedOut;
            if (shouldReconnect) connectToWhatsApp();
        } else if (connection === 'open') {
            console.log("✅ Bot-ku waa xiriirsan yahay!");
        }
    });

    sock.ev.on('creds.update', saveCreds);

    // Halkan waa meesha aad amarrada (commands) ku darayso
    sock.ev.on('messages.upsert', async m => {
        const msg = m.messages[0];
        if (!msg.message || msg.key.fromMe) return;

        const content = msg.message.conversation || msg.message.extendedTextMessage?.text;
        const from = msg.key.remoteJid;

        if (content === 'Asc') {
            await sock.sendMessage(from, { text: 'Waacalykumusalaam! Iska warran sxb?' });
        }
        
        if (content === '.ping') {
            await sock.sendMessage(from, { text: 'Bot-ku waa noool yahay! 🚀' });
        }
    });
}

connectToWhatsApp();
