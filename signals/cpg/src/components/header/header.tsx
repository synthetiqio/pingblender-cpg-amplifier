import { Header as GraffitiHeader } from '@graffiti/react-components/header';
 
function Header (){
    return (
        <div className="header-wrapper">
            <GraffitiHeader titleTemplate={() => 'Graffiti&reg; Pingblender'} />
        </div>
    );
}

export { Header }