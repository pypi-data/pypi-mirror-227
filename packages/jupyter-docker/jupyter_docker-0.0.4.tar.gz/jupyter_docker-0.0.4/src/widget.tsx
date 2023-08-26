import { JupyterFrontEnd } from '@jupyterlab/application';
import { ReactWidget } from '@jupyterlab/apputils';
import JupyterDocker from './JupyterDocker';

export class JupyterDockerWidget extends ReactWidget {
  private _app: JupyterFrontEnd;
  constructor(app: JupyterFrontEnd) {
    super();
    this._app = app;
    this.addClass('dla-Container');
  }

  render(): JSX.Element {
    return <>
      <JupyterDocker app={this._app} />
    </>
  }
}
