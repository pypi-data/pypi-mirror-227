import { createRoot } from 'react-dom/client';
import Main from './JupyterKubernetes';

const div = document.createElement('div');
document.body.appendChild(div);
const root = createRoot(div)

root.render(<Main />);
