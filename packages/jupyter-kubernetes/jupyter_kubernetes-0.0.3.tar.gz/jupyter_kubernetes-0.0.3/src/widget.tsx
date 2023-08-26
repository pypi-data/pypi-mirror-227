import { JupyterFrontEnd } from '@jupyterlab/application';
import { ReactWidget } from '@jupyterlab/apputils';
import { IJupyterDocker } from '@datalayer/jupyter-docker';
import { IJupyterKubernetes } from './index';
import JupyterKubernetes from './JupyterKubernetes';

export class JupyterKubernetesWidget extends ReactWidget {
  private _app: JupyterFrontEnd;
  constructor(app: JupyterFrontEnd, jupyterKubernetes: IJupyterKubernetes, jupyterDocker: IJupyterDocker) {
    super();
    this._app = app;
    this.addClass('dla-Container');
  }

  render(): JSX.Element {
    return (
      <>
        <JupyterKubernetes app={this._app} />
      </>
    )
  }
}
