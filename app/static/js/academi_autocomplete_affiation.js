$('#search_typeahead').typeahead({
      ajax: {
          url: '/ajax/affiation',     // request this url
          displayField: 'name',     // set this json field to display
          valueField: 'affiation_id'  // set this json field to val
      }
      display: 'name',
      val: 'id',
      items: '10'
    });
