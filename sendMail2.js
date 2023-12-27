const nodemailer = require("nodemailer");
require('dotenv').config();

const sendMail = async (email, password, mailOptions) => {
    try {
        const transporter = nodemailer.createTransport({
            service: 'Gmail',
            host: "smtp.gmail.com",
            port: 465,
            secure: true,
            auth: {
                user: email,
                pass: password,
            },
            rejectUnauthorized: false,
            textEncoding: 'utf-8',
        });

        const destinos = mailOptions.to.split(', ');

        for (const destinatario of destinos) {
            const info = await transporter.sendMail({
                ...mailOptions,
                to: destinatario,
            });

            console.log(`E-mail enviado para ${destinatario}:`, info);
        }
    } catch (error) {
        console.error('Erro ao enviar o e-mail:', error);
    }
}

module.exports = sendMail;
