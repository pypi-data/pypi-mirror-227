import { useState, useEffect } from 'react';
import { JupyterFrontEnd } from '@jupyterlab/application';
import { ThemeProvider, BaseStyles, Box } from '@primer/react';
import { UnderlineNav } from '@primer/react/drafts';
import { WheelOfDharmaIcon } from '@datalayer/icons-react';
import PodsTab from './components/PodsTab';
import ServicesTab from './components/ServicesTab';
import AboutTab from './components/AboutTab';
import { requestAPI } from './handler';

export type JupyterFrontEndProps = {
  app?: JupyterFrontEnd;
}

const JupyterKubernetes = (props: JupyterFrontEndProps) => {
  const [tab, setTab] = useState(1);
  const [version, setVersion] = useState('');
  useEffect(() => {
    requestAPI<any>('config')
    .then(data => {
      setVersion(data.version);
    })
    .catch(reason => {
      console.error(
        `Error while accessing the jupyter server jupyter_kubernetes extension.\n${reason}`
      );
    });
  });
  return (
    <>
      <ThemeProvider>
        <BaseStyles>
          <Box>
            <Box>
              <UnderlineNav>
              <UnderlineNav.Item aria-current="page" onSelect={e => {e.preventDefault(); setTab(1);}}>
                  Pods
                </UnderlineNav.Item>
                <UnderlineNav.Item onSelect={e => {e.preventDefault(); setTab(2);}}>
                  Services
                </UnderlineNav.Item>
                <UnderlineNav.Item icon={() => <WheelOfDharmaIcon colored/>} onSelect={e => {e.preventDefault(); setTab(3);}}>
                  About
                </UnderlineNav.Item>
              </UnderlineNav>
            </Box>
            <Box m={3}>
              {tab === 1 && <PodsTab/>}
              {tab === 2 && <ServicesTab/>}
              {tab === 3 && <AboutTab version={version} />}
            </Box>
          </Box>
        </BaseStyles>
      </ThemeProvider>
    </>
  );
}

export default JupyterKubernetes;
