$('#search_typeahead_scholar').typeahead({
      ajax: {
          url: '/ajax/scholar',     // request this url
          displayField: 'name',     // set this json field to display
          valueField: 'name',  // set this json field to val
          triggerLength: 3
      },
      item: '<li><a href="#"></a></li>',
      display: 'name',
      val: 'id',
      items: '10'
    });

$('#search_typeahead_scholar_single').typeahead({
      ajax: {
          url: '/ajax/scholar',     // request this url
          displayField: 'name',     // set this json field to display
          valueField: 'name',  // set this json field to val
          triggerLength: 3
      },
      item: '<li><a href="#"></a></li>',
      display: 'name',
      val: 'id',
      items: '10'
    });

$('#search_typeahead_affiliation').typeahead({
      ajax: {
          url: '/ajax/affiliation',     // request this url
          displayField: 'name',     // set this json field to display
          valueField: 'name',  // set this json field to val
          triggerLength: 3
      },
      item: '<li><a href="#"></a></li>',
      display: 'name',
      val: 'id',
      items: '10'
    });
