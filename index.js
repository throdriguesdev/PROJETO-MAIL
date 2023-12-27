const express = require('express');
const multer = require('multer');
const nodemailer = require('nodemailer');
const app = express();
const port = 3000;

app.use(express.static('public'));
app.use(express.json());
app.use(express.urlencoded({ extended: true }));
const storage = multer.memoryStorage();
const upload = multer({ storage: storage });

// Lista de e-mails enviados
const emailsEnviados = new Set();

app.get('/', (req, res) => {
    res.sendFile(__dirname + '/index.html');
});

app.post('/enviar_email', upload.array('anexos'), async (req, res) => {
    const userEmail = req.body.userEmail;
    const userPassword = req.body.userPassword;
    const assunto = req.body.assunto;
    const corpo = req.body.corpo;
    const assinatura = req.body.assinatura || '';
    let emails = req.body.emails;

    if (!Array.isArray(emails)) {
        emails = [emails];
    }

    emails = emails.map(email => email.trim());

    const transporter = nodemailer.createTransport({
        service: 'Gmail',
        host: 'smtp.gmail.com',
        port: 465,
        secure: true,
        auth: {
            user: userEmail,
            pass: userPassword,
        },
        rejectUnauthorized: false,
        textEncoding: 'utf-8',
    });

    // Define a function to send an email and return a Promise
    const sendEmail = async (email) => {
        // Check if the email has been sent before
        if (emailsEnviados.has(email)) {
            console.log(`E-mail ${email} já foi enviado. Ignorando...`);
            return;
        }

        const anexo = {
            filename: req.files[emails.indexOf(email)].originalname,
            content: Buffer.from(req.files[emails.indexOf(email)].buffer, 'binary'),
            contentType: 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
        };

        const mailOptions = {
            from: {
                name: 'UmTelecom',
                address: process.env.USER
            },
            to: email,
            subject: assunto,
            text: corpo + '\n\n' + assinatura,
            attachments: [anexo],
            encoding: 'utf-8',
        };

        try {
            await transporter.sendMail(mailOptions);
            console.log(`Email sent to ${email}`);

            // Add the sent email to the list
            emailsEnviados.add(email);
        } catch (error) {
            console.error('Erro ao enviar e-mail:', error);
            throw error; // Rethrow the error to handle it later
        }
    };

    // Use a for...of loop for sequential email sending
    for (const email of emails) {
            try {
            await sendEmail(email);
        } catch (error) {
            console.error('Erro ao enviar e-mail:', error);
            res.status(500).send('Erro ao enviar e-mails');
            return;
        }
    }

    // If all emails are sent successfully, respond with success
    res.status(200).send('E-mails enviados com sucesso');
});

app.listen(port, () => {
    console.log(`Server running at http://localhost:${port}`);
});
