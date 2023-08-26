import { Token } from '@lumino/coreutils';
import { JupyterFrontEnd, JupyterFrontEndPlugin } from '@jupyterlab/application';
import { ISettingRegistry } from '@jupyterlab/settingregistry';
import { MainAreaWidget, ICommandPalette } from '@jupyterlab/apputils';
import { ILauncher } from '@jupyterlab/launcher';
import icon from '@datalayer/icons-react/data2/WhaleSpoutingIconLabIcon';
import { requestAPI } from './handler';
import { JupyterDockerWidget } from './widget';
import { timer, Timer, TimerView, ITimerViewProps } from "./store";

import '../style/index.css';

export type IJupyterDocker = {
  timer: Timer,
  TimerView: (props: ITimerViewProps) => JSX.Element,
};

export const IJupyterDocker = new Token<IJupyterDocker>(
  '@datalayer/jupyter-docker:plugin'
);

/**
 * The command IDs used by the plugin.
 */
namespace CommandIDs {
  export const create = 'create-jupyter-docker-widget';
}

/**
 * Initialization data for the @datalayer/jupyter-docker extension.
 */
const plugin: JupyterFrontEndPlugin<IJupyterDocker> = {
  id: '@datalayer/jupyter-docker:plugin',
  autoStart: true,
  requires: [ICommandPalette],
  optional: [ISettingRegistry, ILauncher],
  provides: IJupyterDocker,
  activate: (
    app: JupyterFrontEnd,
    palette: ICommandPalette,
    settingRegistry: ISettingRegistry | null,
    launcher: ILauncher
  ): IJupyterDocker => {
    const jupyterDocker: IJupyterDocker  = {
      timer,
      TimerView,
    }
    const { commands } = app;
    const command = CommandIDs.create;
    commands.addCommand(command, {
      caption: 'Show Jupyter Docker',
      label: 'Jupyter Docker',
      icon,
      execute: () => {
        const content = new JupyterDockerWidget(app);
        const widget = new MainAreaWidget<JupyterDockerWidget>({ content });
        widget.title.label = 'Jupyter Docker';
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
    console.log('JupyterLab extension @datalayer/jupyter-docker is activated!');
    if (settingRegistry) {
      settingRegistry
        .load(plugin.id)
        .then(settings => {
          console.log('@datalayer/jupyter-docker settings loaded:', settings.composite);
        })
        .catch(reason => {
          console.error('Failed to load settings for @datalayer/jupyter-docker.', reason);
        });
    }
    requestAPI<any>('config')
      .then(data => {
        console.log(data);
      })
      .catch(reason => {
        console.error(
          `The Jupyter Server extension jupyter_docker appears to be missing.\n${reason}`
        );
      });
    return jupyterDocker;
  }
};

export default plugin;
