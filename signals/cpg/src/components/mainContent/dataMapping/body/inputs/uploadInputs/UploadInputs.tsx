import { Upload } from '@graffiti/react-components/upload';
import './uploadInputs.scss';
// import { useEffect } from 'react';
import { useInputUploadStore } from '@/stores/inputUpload';

function UploadInputs(){
    const setFileList = useInputUploadStore((state) => state.setFileList);

    const onChange = (_file: File, fileList: FileList): void => {
        setFileList(fileList);
    }; 

    const uploadInputs = (fileList:any) => {
        console.log('uploadInput', fileList);
    }; 

    return (
        <div className="InputUpload">
            <Upload 
                className="InputUpload__component"
                onChange={onChange}
                autoUpload
                onUpload={uploadInputs}
                acceptFileType=".csv"
                uploadInstruction="Uploading multiple files in CSV format are accepted"
                uploadTitle="upload your inputs"
                maxFileSize={10 * 1024 * 1024}
                config={{
                    trigger:false, 
                    type:'inline', 
                    size: true,
                }}
            />
        </div>

    );
}

export { UploadInputs };