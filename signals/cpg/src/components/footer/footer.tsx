import { Footer } from '@graffiti/react-components/footer';
import { footerContent } from '@/utils/constants';

function Footer(){
    const footerType = 'text';

    return (
        <div className="footer-wrapper">
            <GraffitiFooter content={footerContent} type={footerType}/>
        </div>
    );
}

export { Footer };