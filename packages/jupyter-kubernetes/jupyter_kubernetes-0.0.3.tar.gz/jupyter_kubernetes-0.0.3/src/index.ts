import { Token } from '@lumino/coreutils';
import { JupyterFrontEnd, JupyterFrontEndPlugin } from '@jupyterlab/application';
import { ISettingRegistry } from '@jupyterlab/settingregistry';
import { MainAreaWidget, ICommandPalette } from '@jupyterlab/apputils';
import { ILauncher } from '@jupyterlab/launcher';
import { IJupyterDocker } from '@datalayer/jupyter-docker';
import icon from '@datalayer/icons-react/data2/WheelOfDharmaIconLabIcon';
import { requestAPI } from './handler';
import { JupyterKubernetesWidget } from './widget';
import { timer, Timer, TimerView, ITimerViewProps } from "./store";

import '../style/index.css';

export type IJupyterKubernetes = {
  timer: Timer,
  TimerView: (props: ITimerViewProps) => JSX.Element,
};

export const IJupyterKubernetes = new Token<IJupyterKubernetes>(
  '@datalayer/jupyter-kubernetes:plugin'
);

export const jupyterKubernetes: IJupyterKubernetes = {
  timer,
  TimerView,
}

/**
 * The command IDs used by the plugin.
 */
namespace CommandIDs {
  export const create = 'create-jupyter-kubernetes-widget';
}

/**
 * Initialization data for the @datalayer/jupyter-kubernetes extension.
 */
const plugin: JupyterFrontEndPlugin<void> = {
  id: '@datalayer/jupyter-kubernetes:plugin',
  autoStart: true,
  requires: [IJupyterDocker, ICommandPalette],
  optional: [ISettingRegistry, ILauncher],
  activate: (
    app: JupyterFrontEnd,
    jupyterDocker: IJupyterDocker,
    palette: ICommandPalette,
    settingRegistry: ISettingRegistry | null,
    launcher: ILauncher
  ) => {
    const { commands } = app;
    const command = CommandIDs.create;
    commands.addCommand(command, {
      caption: 'Show Jupyter Kubernetes',
      label: 'Jupyter Kubernetes',
      icon,
      execute: () => {
        const content = new JupyterKubernetesWidget(app, jupyterKubernetes, jupyterDocker);
        const widget = new MainAreaWidget<JupyterKubernetesWidget>({ content });
        widget.title.label = 'Jupyter Kubernetes';
        widget.title.icon = icon;
        app.shell.add(widget, 'main');
      }
    });
    const category = 'Datalayer';
    palette.addItem({ command, category });
    if (launcher) {
      launcher.add({
        command,
        category,
        rank: 3,
      });
    }
    console.log('JupyterLab extension @datalayer/jupyter-kubernetes is activated!');
    if (settingRegistry) {
      settingRegistry
        .load(plugin.id)
        .then(settings => {
          console.log('@datalayer/jupyter-kubernetes settings loaded:', settings.composite);
        })
        .catch(reason => {
          console.error('Failed to load settings for @datalayer/jupyter-kubernetes.', reason);
        });
    }
    requestAPI<any>('config')
      .then(data => {
        console.log(data);
      })
      .catch(reason => {
        console.error(
          `The Jupyter Server extension jupyter_kubernetes appears to be missing.\n${reason}`
        );
      });
  }
};

export default plugin;
