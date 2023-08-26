import { createRoot } from 'react-dom/client';
import JupyterDocker from './JupyterDocker';

const div = document.createElement('div');
document.body.appendChild(div);
const root = createRoot(div)

root.render(<JupyterDocker />);
