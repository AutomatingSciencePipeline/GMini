import { AppProps } from 'next/app';
import "../styles/globals.css";

function GMiniApp({ Component, pageProps }: AppProps) {
    return <Component {...pageProps} />
}

 export default GMiniApp