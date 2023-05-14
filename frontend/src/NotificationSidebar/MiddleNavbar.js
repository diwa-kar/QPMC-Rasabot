import React, { useEffect, useState } from 'react';
import NotificationItem from './NotificationItem';
import { Form } from 'reactstrap';
import { values } from 'lodash';


const MiddleNavbar = (props) => {
  const [iconState, setIconState] = useState('fa fa-search');

  const [isSearchMode, setIsSearchMode] = useState(false);
  const [searchTerm, setSearchTerm] = useState('');

  const [purchaseRequisitions, setPurchaseRequisitions] = useState([]);

  const makeAPICall = async () => {
    try {
      const response = await fetch('http://localhost:5000/api', { mode: 'cors' });
      const data = await response.json();
      console.log({ data })
      const purchaseRequisitions = data.feed.entry.map(entry => {
        return {
          purchaseRequisition: entry.content[0]['m:properties'][0]['d:PurchaseRequisition'][0],
          purchaseRequisitionType: entry.content[0]['m:properties'][0]['d:PurchaseRequisitionType'][0],
          SourceDetermination: entry.content[0]['m:properties'][0]['d:SourceDetermination'][0],
          date: entry.updated[0]
        };
      });
      console.log(purchaseRequisitions);
      setPurchaseRequisitions(purchaseRequisitions);

    }

    catch (e) {
      console.log(e)
    }
  }
  useEffect(() => {
    makeAPICall();
  }, [])


  const handleClick = () => {
    setIsSearchMode(true);
    setIconState('fa fa-user')
    console.log(props)
  };

  const handleInputChange = (event) => {
    setSearchTerm(event.target.value);
  };

  const handleItem = () => {
    console.log('Button clicked!');
    console.log(props)
  }
  const setUpdateIt = (values) => {
    console.log('I am printing values', values)
    props.updateValues(purchaseRequisitions[values]);
  }

  return (

    <div className='middle-sidebar'>

      <div style={{ width: '300px', height: '100vh', overflowY: 'scroll', marginLeft: '2vh' }}>
        {/* Your code goes here */}
        <ul style={{ width: '100%', height: '100%', listStyle: 'none', padding: 0 }}>

          {
            (isSearchMode) ?
              (<Form className="nosubmit">
                <input className="nosubmit mr-sm-2 search-box" type="text" placeholder="Search..." value={searchTerm} onChange={handleInputChange} />
              </Form>
              ) : (
                <><span className="Notification" onClick={handleClick}>
                  Notifications
                  <i className={iconState} aria-hidden="true" style={{ marginLeft: '3.9vw' }}></i>
                </span></>
              )
          }
          <NotificationItem purchaseRequisitions={purchaseRequisitions} updateIt={props.updateValues} />
        </ul>
      </div>
    </div>

  );
};

export default MiddleNavbar;