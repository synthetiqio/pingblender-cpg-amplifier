import { useState, useEffect } from 'react';
import {
    Browserrouter as Router, 
    Routes, 
    Route, 
    useLocation, 
    useNavigate,
} from 'react-router-dom';

import { QueryClient, QueryClientProvider } from '@tanstack/react-query';
import { NavigationItem } from '@23Controls/react-components/navigation';
import { useDpStepperCountStore } from '@/stores/dataProcessing/dpStepperIndex';
import { ConfigureProvider } from './config/config-context';

import { useStepperCountStore } from '@stores/stepperIndex'; 
import { useFileStore } from '@stores/documentProcessing/files';
import { useAuthStore } from '@stores/auth';
import { Header, Sidebar, Footer, Notifier} from '@/components';
import { Error404 } from '@/pages';

import { alerts } from '@/constants';
import { Home } from '@/pages/Home'; 
import { DataMapping } from './components/mainContent/DAtaMapping';
import { DocumentProcessing } from './pages/DocumentProcessing';

import { ParsingData } from './pages/DocumentProcessing/ParsingData'; 
import { Review } from './pages/DocumentProcessing/Review'; 

import {
    getAndSetBatchId,
    handleManualIndexForPath,
} from './utils/routingUtils/routingUtils';

import './App.scss'

const queryClient = new QueryClient();

function RouteChangeListener({
    setBatchId,
}:{
    setBatchId: React.Dispatch<React.SetStateaction<string | null>>;
}){
    const location = useLocation();
    const setIndex = useStepperCountStore((state) => state.setIndex);

    useEffect(() => {
        handleManualIndexForPath({ setIndex }); 
        getAndSetBatchId({ location, setBatchId });
    }, [location, setIndex]);

    return null;
}

function Layout({ children }: {
    children: any 
}){
    const [current] = useState('0');
    const navigate = useNavigate();
    const setDocumentProcessingIndex = useDpStepperCountStore(
        (state) => state.setIndex
    );
    const setFileSfids = useFilesStore((state:any) => state.setFileSfids);
    const setStep2Validated = useDpStepperCountStore(
        (state) => state.setStep2Validated
    ); 

    const navigationItems: NavigationItem[] = [
        {
            name: 'Home',
            divider: true, 
            prefixIcon: 'home',
            prefixCollapsedIcon: 'home', 
            anchorProps: {
                href: '/', 
            },
        },
    ];

    const onClickItem = (event: React.HouseEvent<HTMLElement, MouseEvent>) => {
            navigate('/');
            setDocumentProcessingIndex(0);
            setFileSfids([]);
            setStep2Validated(false);
            queryClient.clear();
            event.preventDefault();
        }; 



    const onCollapseEvent = () => {};

    return (
        <div className="ap-qd">
          <Header />
            <div className='main-wrapper'>
              <div className='content-wrapper'>
                <Sidebar  
                  itemClick={(e) => onClickItem(e)}
                  navList={navigationItems}
                  selectedNavItem={current}
                  collapsedVal={false}
                  onCollapseEvent={onCollapseEvent}
                 />
               <div className="content-wrapper-child">
                  <div className="main-content">{children}</div>        
                  <Footer />     
               </div>
              </div>
            </div>
        </div>
   );
}

function MfeLayout({ children } : { children: any }){
    return <div className="mfe-main-content">{ children }</div>;
}

function App(props: any){
    const { basePath = '', batch_id = null, accessToken = null } = props;
    const [ batchId, setBatchId ] = useState<string | null>(batch_id);
    const isMicroFrontend = () => import.meta.env.VITE_APP_MODE === 'child';

    const fileSfids = useFileStore((state:any) => state.fileSfids); 
    const setToken = useAuthStore((state) => state.setToken);

    const sendHeightToParent = () => {
        requestAnimationFrame(() => {
            const height = 
              document.documentElement?.offsetHeight ?? document.body?.offsetHeight;
            const event = new CustomEvent<{ height: number }>(
                'myApp:mfeHeightChange',
                { detail: { height }}
            );
            window.dispatchEvent(event);
    });
  };

  useEffect(() => {
    sendHeightToParent();
    const handleResize = () => {
        sendHeightToParent();
    };
    window.addEventListener('resize', handleResize);
    return () => {
        window.removeEventListener.('resize', handleResize);
    };
  }, []);

  useEffect(() => {
    if (accessToken) {
        setToken(accessToken);
    }
  }, [accessToken]);

  const [activeTab, setActiveTab] = useState<string>('graffiti-home');

  const changeRoute = (tab: string) => {
    setActiveTab(tab);
  };

  const getActiveComponent = () => {
    switch(activeTab) {
        case 'graffiti-home':
            return <MfeLayout children={<Home mfeRouter={changeRoute} />} />;
        case 'graffiti-pretzl':
            return <DocumentProcessing batchId={batchId} fileSfids={fileSfids} />;
        case 'graffiti-mapping':
            return <DataMapping />;
        default:
            return <Error404 />;
    }
  }; 

  return (
    <QueryClientProvider client={queryClient}>
        <ConfigureProvider>
            <Notifier defaults={alerts} />
            <Router>
                <RouteChangeListener setBatchId={setBatchId} />
                <Routes>
                    {!isMicroFrontend() ? (
                        <>
                        <Route
                          path="/graffiti-pretzl"
                          element={
                            <Layout 
                              children={
                                <DocumentProcessing
                                  batchId={null}
                                  fileSfids={fileSfids}
                                />
                              }
                              />
                            }
                          />
                        <Route
                          path="/graffiti-pretzl/*"
                          element={
                            <Layout 
                              children={
                                <DocumentProcessing
                                  batchId={batchId}
                                  fileSfids={fileSfids}
                                />
                              }
                              />
                            }
                        />
                        <Route 
                          path='/graffiti-mapping'
                          element={<Layout children={<DataMapping />} />}
                        />
                        <Route 
                          path='graffiti-mapping/*'
                          element={<Layout children={<DataMapping />} />}
                        />
                        <Route path='/' element={<Layout children={<Home />} />} />
                       </>
                        ):(
                            <Route 
                              path={`/${basePath}/*`}
                              element={<MfeLayout children={getActiveComponent()} />}
                            />

                        )}
                        <Route path="*" element={<p>test</p>} />
                </Routes>
            </Router>
        </ConfigureProvider>
    </QueryClientProvider>
  );
}

export default App;
