$('#search_typeahead').typeahead({
      ajax: {
          url: '/ajax/scholar',     // request this url
          displayField: 'name',     // set this json field to display
          valueField: 'scholar_id'  // set this json field to val
      }
      display: 'name',
      val: 'id',
      items: '10'
    });
