import { useState, useEffect } from 'react';
import { JupyterFrontEnd } from '@jupyterlab/application';
import { ThemeProvider, BaseStyles, Box } from '@primer/react';
import { UnderlineNav } from '@primer/react/drafts';
import { WhaleSpoutingIcon } from '@datalayer/icons-react';
import ImagesTab from './tabs/ImagesTab';
import ContainersTab from './tabs/ContainersTab';
import AboutTab from './tabs/AboutTab';
import { requestAPI } from './handler';

export type JupyterFrontEndProps = {
  app?: JupyterFrontEnd;
}

const JupyterDocker = (props: JupyterFrontEndProps) => {
  const [tab, setTab] = useState(1);
  const [version, setVersion] = useState('');
  useEffect(() => {
    requestAPI<any>('config')
    .then(data => {
      setVersion(data.version);
    })
    .catch(reason => {
      console.error(
        `Error while accessing the jupyter server jupyter_docker extension.\n${reason}`
      );
    });
  }, []);
  return (
    <>
      <ThemeProvider>
        <BaseStyles>
          <Box>
            <Box>
              <UnderlineNav>
                <UnderlineNav.Item aria-current="page" onSelect={e => {e.preventDefault(); setTab(1);}}>
                  Images
                </UnderlineNav.Item>
                <UnderlineNav.Item onSelect={e => {e.preventDefault(); setTab(2);}}>
                  Containers
                </UnderlineNav.Item>
                <UnderlineNav.Item icon={() => <WhaleSpoutingIcon colored/>} onSelect={e => {e.preventDefault(); setTab(3);}}>
                  About
                </UnderlineNav.Item>
              </UnderlineNav>
            </Box>
            <Box m={3}>
              {tab === 1 && <ImagesTab/>}
              {tab === 2 && <ContainersTab/>}
              {tab === 3 && <AboutTab version={version} />}
            </Box>
          </Box>
        </BaseStyles>
      </ThemeProvider>
    </>
  );
}

export default JupyterDocker;
