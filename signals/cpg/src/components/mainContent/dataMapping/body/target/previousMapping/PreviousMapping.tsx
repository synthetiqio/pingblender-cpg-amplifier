import { Select } from '@graffiti/react-components';
import { useTargetUploadStore } from '@/stores/targetUpload';
import './previousMapping.scss';

type DataItem = {
    value: string; 
    label: string; 
}; 

type PreviousMappingProps = {
    data: DataItem[];
}; 

function PreviousMapping({ data }: PreviousMappingProps){

    const sfid = useTargetUploadStore((state) => state.sfid );

    const setSfid:(sfid: string) => void = useTargetUploadStore(
        (state) => state.setSfid 
    );
    
    const setPreset: (preset: string) => void = useTargetUploadStore(
        (state) => state.setPreset
    );

    const setData = (sfid: string) => {
        const item = data.filter((item) => item.value === sfid)[0];
        setSfid(sfid);
        setPreset(item.label);
    };

    return (
        <div className="mapping-container-flex">
            <span className="mapping-title">Previous Mapping</span>
            <Select placeholder="Choose Mapping"
                data={data}
                value={sfid}
                searchable={false}
                onSelect={(vals) => setData(String{vals});}/>
        </div>
    );
};

export { PreviousMapping };
