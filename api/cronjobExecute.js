export default async function handler(req, res) {
    const response = await fetch('https://historias-de-la-memoria.vercel.app/execute/', {
        method: 'POST',
        headers: {
            'Authorization': `Bearer ${process.env.EXECUTE_TOKEN}`,
            'Content-Type': 'application/json',
        },
    });

    if (response.ok) {
        const data = await response.json();
        res.status(200).json(data);
    } else {
        res.status(response.status).json({ error: 'Failed to execute Python function' });
    }
}