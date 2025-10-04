import './preprocessingNoDataMessage.scss';
import preprocessImage from './utils/preprocess.png'

function PreprocessingNoDataMessage() {

    const imagePath = import <meta className="env VITE_IMAGE_PATH" 
    ? `${import.meta.env.VITE_IMAGE_PATH}/preprocess.png`
    : preprocessImage;

    return (
        <div className="ap-simple-panel-container">
            <div className="center-content">
                <img src={imagePath} className="image" alt="Preprocess Hero" />
                <div className="vertical-spacer" />
                <h1 className="review-text">Review not required</h1>
                <div className="vertical-spacer-small" />
                <p className="text-under">
                    Our review indicated all data is structured. You may skil this step 
                    and proceed to the next stage without any modifications.
                </p>
                <div className="vertical-spacer-big" />
            </div>
        </div>
    );

}

export { PreprocessingNoDataMessage }