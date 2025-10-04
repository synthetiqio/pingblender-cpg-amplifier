import { Table, Column } from '@graffiti/react-components/table'; 
import { useEffect, useState } from 'react';
import { useReviewStore } from '@/stores/reviewMapping';

import './reviewAndConfirm.scss';

function ReviewAndConfirm() {
    const dataList = useReviewStore((state) => state.dataList);
    const [loading, setLoading] = useState(true);

    useEffect(() => {
        if(dataList !== undefined){
            setLoading(false);
        }
    }, [dataList] );

    if (loading) {
        return <div>Loading...</div>;
    }

    const transformArray = (arr:any) =>{
        return arr.map((obj:any) => ({
            targetField: obj.originalHeader, 
            sourceFields: obj.sourceFields.suggested_header,
        }));
    };

    return (
        <div className="review-confirm-container">
            <div className="review-confirm-table">
                <div className="ap-table-demo-review">
                    <Table originalData={transformArray(dataList.target_fields)} hasTitle>
                        <Column field="targetField">
                        Target Field
                        </Column>
                        <Column field="sourceFields">
                        Mapped Source Field(s)
                        </Column>
                    </Table>
                </div>
            </div>
        </div>
    );
}

export { ReviewAndConfirm }