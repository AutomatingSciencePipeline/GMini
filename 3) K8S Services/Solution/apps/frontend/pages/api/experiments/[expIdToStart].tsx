import { NextApiHandler } from 'next';

const startExperimentHandler: NextApiHandler = async (req, res) => {
	const { expIdToStart } = req.query;
	const { key } = req.body;

	console.log("The expIdToStart is ", expIdToStart);
	try {
		const url = `http://gmini-backend:8080/experiment`;
		const backendResponse = await fetch(url, {
			method: 'POST',
			headers: new Headers({
				'Content-Type': 'application/json',
			}),
			// credentials:
			body: JSON.stringify({ experiment: { id: expIdToStart, key } }),
		});
		if (backendResponse?.ok) {
			res.status(backendResponse.status).json({ response: backendResponse });
		} else {
			throw new Error(`Fetch failed: ${backendResponse.status}`);
		}
	} catch (error) {
		const message = 'Could not reach the server to request start of the experiment';
		console.log('Error contacting server: ', error);
		res.status(500).json({ response: message });
		throw new Error(message);
	}
};

export default startExperimentHandler;