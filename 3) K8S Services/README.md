# 3) K8S Services
## 1) Modify Backend Image to Receive API Calls
In the backend's app.py script, add a post endpoint. If you get stuck, check out this Flask tutorial by [GeeksForGeeks](https://www.geeksforgeeks.org/flask-tutorial/). If you still need help, feel free to look at the solution.

Don't forget to build and push the backend's image.

## 2) Modify Frontend Image to Send API Calls
To send API calls to the backend we need to restructure the NextJS app to include middleware. Otherwise, we'd run into [CORS issues](https://developer.mozilla.org/en-US/docs/Web/HTTP/CORS?utm_medium=firefox-desktop&utm_source=firefox-suggest&utm_campaign=firefox-mdn-web-docs-suggestion-experiment&utm_content=treatment).

To start, rename the apps/frontend/app folder to apps/frontend/pages.

```
mv apps/frontend/app apps/frontend/pages
```

The new folder will indicate to the NextJS app that you want to have routing, where each file is a page and each folder is a directory.
For more information check out the [NextJS documentation](https://nextjs.org/docs/pages/building-your-application/routing/pages-and-layouts). Next we want to create a route for our frontend's calls to the middleware.

```
mkdir /apps/frontend/pages/api
```

```
mkdir /apps/frontend/pages/api/experiments
```

```
touch /apps/frontend/pages/api/experiments/[expIdToStart].tsx
```

The naming convention for the file is important as the brackets indicate a query parameter check [dynamic variables](https://nextjs.org/docs/pages/building-your-application/routing/api-routes) for more information. The following code will receive an API call from the frontend and send the API call to the backend:

```
import { NextApiHandler } from 'next';

const startExperimentHandler: NextApiHandler = async (req, res) => {
	const { expIdToStart } = req.query;
	const { key } = req.body;

	console.log("The expIdToStart is ", expIdToStart);
	try {
		const url = `http://gmini-backend:5050/experiment`;
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
```

Note that the url refers to 'gmini-backend'. This name has to be the same name as your backend's service. Also note the subdirectory. The subdirectory's name has to be the same as your Flask app's endpoint.

We're still not done refactoring to a pages based NextJS app. Because files within the pages folder are related to the pages the user routes to, we have to move the favicon.ico and the globals.css files to new locations. 

```
mv frontend/pages/favicon.ico frontend/public/
```

```
mkdir frontend/styles
```

```
mv frontend/pages/globals.css frontend/styles/
```

Currently, we don't have a root directory. Hence we need to rename page.tsx to index.tsx.

```
mv frontend/pages/page.tsx frontend/public/index.tsx
```

We also want a custom layout for our app (ie. using our globals.css style). Hence we need to create a _app.tsx file.

```
touch apps/frontend/pages/_app.tsx
```

Use the following code for the _app.tsx file to include our global styles:

```
import { AppProps } from 'next/app';
import "../styles/globals.css";

function GMiniApp({ Component, pageProps }: AppProps) {
    return <Component {...pageProps} />
}

export default GMiniApp
```

We no longer need the layout.tsx file so we can delete it

```
rm apps/frontend/pages/layout.tsx
```

To connect the user to the middleware, try adding a button within index.tsx that calls the middleware endpoint. Feel free to check the solution if you get stuck.

Don't forget to build and push the frontend's image.

## 3) Create Backend Service
To expose pods to each other or externally, [Kubernetes services](https://kubernetes.io/docs/concepts/services-networking/service/) are used. In this case, we want to create a headless ClusterIP service as we only want the backend to be accessed internally within the cluster and we do not care for what the IP address would be. Create the service file:

```
touch k8s/backend/service.yaml
```

Then, add the following code:

```
apiVersion: v1
kind: Service
metadata:
  name: gmini-backend
  namespace: default
  labels:
    app: gmini
spec:
  selector:
    app: gmini
    tier: backend
  ports:
    - protocol: TCP
      port: 5050
      targetPort: 5050
```

Note that the selector is the same as the metadata within the backend's deployment.yaml file.

To ensure everything is updated, you can delete Kubernetes objects via:

```
kubectl delete deployment gmini-backend
```

```
kubectl delete deployment gmini-frontend
```

Don't forget to apply your service, backend, and frontend!

## 4) Create Frontend Service

While we could port-forward the frontend like we did in the previous section, we could also add a LoadBalancer to externally expose the frontend's deployment to our local machine. Try creating your own LoadBalancer service! If you get stuck feel free to check the solution!

When you're done, use the following command to expose the frontend to your machine:

```
minikube service gmini-frontend
```

Note that the name of the service is 'gmini-frontend' in this case.
