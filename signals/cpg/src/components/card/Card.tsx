import { Button } from '@graffiti/react-components/button';
import { Link } from 'react-router-dom'; 
import './Card.scss'

function CardContent ({
    title, 
    text, 
    image, 
    link, 
    isLoading = false, 
    buttonLabel, 
    onClick, 
    mfeClick,
 } : {
    title:string; 
    text:string; 
    image?:string;
    link?: string; 
    isLoading?: boolean;
    buttonLabel?: string;
    onClick?: () => void;
    mfeClick?: () => void;
 }) {
    return (
        <div 
         className="card_body"
         style={{ cursor: link !== undefined ? 'pointer' : 'auto' }}
         onClick={mfeClick}
         >
            { image && (
            <img src={image} style={{ width: '100%', marginBottom:'0.5rem'}} />
            )}
            <p className="card__body__title">{title}</p>
            <p className="card__body__text">{text}</p>
            {onClick && (
                <Button
                    loading={isLoading}
                    kind="secondary"
                    icon="icon-pdf-outline"
                    onClick={onClick}
                >
                    {buttonLabel}
                </Button>
            )}
        </div>
    );
 }

 export function Card({
    title, 
    text, 
    image, 
    link, 
    isLoading, 
    width=420, 
    buttonLabel,
    onClick, 
    mfeClick,
 } : {
    title:string; 
    text:string; 
    image?:string;
    link?: string; 
    isLoading?: boolean;
    width?:number;
    buttonLabel?: string;
    onClick?: () => void;
    mfeClick?: () => void;
 }) {  
    return (
        <div className="card" stype={{ width: `${width}px` }}>
            {link !== undefined ? (
                <Link to={link ?? '/'}>
                    <CardContent
                    title={title}
                    text={text}
                    image={image}
                    link={link}
                    isLoading={isLoading}
                    onClick={onClick}
                    mfeClick={mfeClick}
                    buttonLabel={buttonLabel}
                    />
                </Link>
            ): (
                <CardContent
                    title={title}
                    text={text}
                    image={image}
                    link={link}
                    isLoading={isLoading}
                    onClick={onClick}
                    mfeClick={mfeClick}
                    buttonLabel={buttonLabel}
                    />
            )}
        </div>
    );
 }
 