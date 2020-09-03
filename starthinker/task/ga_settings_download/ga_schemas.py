###########################################################################
#
#  Copyright 2020 Google LLC
#
#  Licensed under the Apache License, Version 2.0 (the "License");
#  you may not use this file except in compliance with the License.
#  You may obtain a copy of the License at
#
#      https://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS,
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#  See the License for the specific language governing permissions and
#  limitations under the License.
#
###########################################################################

CUSTOM_DIMENSION_SCHEMA = [{
    'name': 'accountName',
    'type': 'STRING'
}, {
    'name': 'accountId',
    'type': 'STRING'
}, {
    'name': 'propertyName',
    'type': 'STRING'
}, {
    'name': 'propertyId',
    'type': 'STRING'
}, {
    'name': 'id',
    'type': 'STRING'
}, {
    'name': 'name',
    'type': 'STRING'
}, {
    'name': 'index',
    'type': 'STRING'
}, {
    'name': 'scope',
    'type': 'STRING'
}, {
    'name': 'active',
    'type': 'STRING'
}, {
    'name': 'created',
    'type': 'TIMESTAMP'
}, {
    'name': 'updated',
    'type': 'TIMESTAMP'
}, {
    'name': 'date',
    'type': 'DATE'
}, {
    'name': 'selfLink',
    'type': 'STRING'
}]

CUSTOM_METRIC_SCHEMA = [{
    'name': 'accountName',
    'type': 'STRING'
}, {
    'name': 'accountId',
    'type': 'STRING'
}, {
    'name': 'propertyName',
    'type': 'STRING'
}, {
    'name': 'propertyId',
    'type': 'STRING'
}, {
    'name': 'id',
    'type': 'STRING'
}, {
    'name': 'name',
    'type': 'STRING'
}, {
    'name': 'index',
    'type': 'STRING'
}, {
    'name': 'scope',
    'type': 'STRING'
}, {
    'name': 'active',
    'type': 'STRING'
}, {
    'name': 'created',
    'type': 'TIMESTAMP'
}, {
    'name': 'updated',
    'type': 'TIMESTAMP'
}, {
    'name': 'date',
    'type': 'DATE'
}, {
    'name': 'selfLink',
    'type': 'STRING'
}, {
    'name': 'type',
    'type': 'STRING'
}, {
    'name': 'min_value',
    'type': 'INTEGER'
}, {
    'name': 'max_value',
    'type': 'INTEGER'
}]

VIEW_SCHEMA = [{
    'name': 'date',
    'type': 'DATE'
}, {
    'name': 'id',
    'type': 'STRING'
}, {
    'name': 'selfLink',
    'type': 'STRING'
}, {
    'name': 'accountId',
    'type': 'STRING'
}, {
    'name': 'webPropertyId',
    'type': 'STRING'
}, {
    'name': 'accountName',
    'type': 'STRING'
}, {
    'name': 'webPropertyName',
    'type': 'STRING'
}, {
    'name': 'name',
    'type': 'STRING'
}, {
    'name': 'currency',
    'type': 'STRING'
}, {
    'name': 'timezone',
    'type': 'STRING'
}, {
    'name': 'websiteUrl',
    'type': 'STRING'
}, {
    'name': 'defaultPage',
    'type': 'STRING'
}, {
    'name': 'excludeQueryParameters',
    'type': 'STRING'
}, {
    'name': 'siteSearchQueryParameters',
    'type': 'STRING'
}, {
    'name': 'stripSiteSearchQueryParameters',
    'type': 'BOOLEAN'
}, {
    'name': 'siteSearchCategoryParameters',
    'type': 'STRING'
}, {
    'name': 'stripSiteSearchCategoryParameters',
    'type': 'BOOLEAN'
}, {
    'name': 'type',
    'type': 'STRING'
}, {
    'name': 'created',
    'type': 'TIMESTAMP'
}, {
    'name': 'updated',
    'type': 'TIMESTAMP'
}, {
    'name': 'eCommerceTracking',
    'type': 'BOOLEAN'
}, {
    'name': 'enhancedECommerceTracking',
    'type': 'BOOLEAN'
}, {
    'name': 'botFilteringEnabled',
    'type': 'BOOLEAN'
}, {
    'name': 'starred',
    'type': 'BOOLEAN'
}]

GOAL_SCHEMA = [{
    'name': 'date',
    'type': 'DATE'
}, {
    'name': 'id',
    'type': 'STRING'
}, {
    'name': 'accountId',
    'type': 'STRING'
}, {
    'name': 'webPropertyId',
    'type': 'STRING'
}, {
    'name': 'internalWebPropertyId',
    'type': 'STRING'
}, {
    'name': 'profileId',
    'type': 'STRING'
}, {
    'name': 'name',
    'type': 'STRING'
}, {
    'name': 'accountName',
    'type': 'STRING'
}, {
    'name': 'webPropertyName',
    'type': 'STRING'
}, {
    'name': 'profileName',
    'type': 'STRING'
}, {
    'name': 'value',
    'type': 'FLOAT'
}, {
    'name': 'active',
    'type': 'BOOLEAN'
}, {
    'name': 'type',
    'type': 'STRING'
}, {
    'name': 'created',
    'type': 'TIMESTAMP'
}, {
    'name': 'updated',
    'type': 'TIMESTAMP'
}, {
    'name':
        'urlDestinationDetails',
    'type':
        'RECORD',
    'fields': [{
        'name': 'url',
        'type': 'STRING'
    }, {
        'name': 'caseSensitive',
        'type': 'BOOLEAN'
    }, {
        'name': 'matchType',
        'type': 'STRING'
    }, {
        'name': 'firstStepRequired',
        'type': 'BOOLEAN'
    }, {
        'name':
            'steps',
        'type':
            'RECORD',
        'mode':
            'REPEATED',
        'fields': [{
            'name': 'number',
            'type': 'INTEGER'
        }, {
            'name': 'name',
            'type': 'STRING'
        }, {
            'name': 'url',
            'type': 'STRING'
        }]
    }]
}, {
    'name':
        'visitTimeOnSiteDetails',
    'type':
        'RECORD',
    'fields': [{
        'name': 'comparisonType',
        'type': 'STRING'
    }, {
        'name': 'comparisonValue',
        'type': 'STRING'
    }]
}, {
    'name':
        'visitNumPagesDetails',
    'type':
        'RECORD',
    'fields': [{
        'name': 'comparisonType',
        'type': 'STRING'
    }, {
        'name': 'comparisonValue',
        'type': 'STRING'
    }]
}, {
    'name':
        'eventDetails',
    'type':
        'RECORD',
    'fields': [{
        'name': 'useEventValue',
        'type': 'BOOLEAN'
    }, {
        'name':
            'eventConditions',
        'mode':
            'REPEATED',
        'type':
            'RECORD',
        'fields': [{
            'name': 'type',
            'type': 'STRING'
        }, {
            'name': 'matchType',
            'type': 'STRING'
        }, {
            'name': 'expression',
            'type': 'STRING'
        }, {
            'name': 'comparisonType',
            'type': 'STRING'
        }, {
            'name': 'comparisonValue',
            'type': 'STRING'
        }]
    }]
}]

GOOGLE_ADS_LINK_SCHEMA = [{
    'name': 'date',
    'type': 'DATE'
}, {
    'name': 'id',
    'type': 'STRING'
}, {
    'name': 'kind',
    'type': 'STRING'
}, {
    'name': 'selfLink',
    'type': 'STRING'
}, {
    'name':
        'entity',
    'type':
        'RECORD',
    'fields': [{
        'name':
            'webPropertyRef',
        'type':
            'RECORD',
        'fields': [{
            'name': 'id',
            'type': 'STRING'
        }, {
            'name': 'kind',
            'type': 'STRING'
        }, {
            'name': 'href',
            'type': 'STRING'
        }, {
            'name': 'accountId',
            'type': 'STRING'
        }, {
            'name': 'internalWebPropertyId',
            'type': 'STRING'
        }, {
            'name': 'name',
            'type': 'STRING'
        }]
    }]
}, {
    'name':
        'adWordsAccounts',
    'type':
        'RECORD',
    'mode':
        'REPEATED',
    'fields': [{
        'name': 'kind',
        'type': 'STRING'
    }, {
        'name': 'customerId',
        'type': 'STRING'
    }, {
        'name': 'autoTaggingEnabled',
        'type': 'BOOLEAN'
    }]
}, {
    'name': 'name',
    'type': 'STRING'
}, {
    'name': 'profileIds',
    'type': 'RECORD',
    'mode': 'REPEATED',
    'fields': [{
        'name': 'id',
        'type': 'STRING'
    }]
}]

REMARKETING_AUDIENCE_SCHEMA = [{
    'name': 'date',
    'type': 'DATE'
}, {
    'name': 'kind',
    'type': 'STRING'
}, {
    'name': 'id',
    'type': 'STRING'
}, {
    'name': 'accountId',
    'type': 'STRING'
}, {
    'name': 'webPropertyId',
    'type': 'STRING'
}, {
    'name': 'webPropertyName',
    'type': 'STRING'
}, {
    'name': 'accountName',
    'type': 'STRING'
}, {
    'name': 'internalWebPropertyId',
    'type': 'STRING'
}, {
    'name': 'created',
    'type': 'TIMESTAMP'
}, {
    'name': 'updated',
    'type': 'TIMESTAMP'
}, {
    'name': 'name',
    'type': 'STRING'
}, {
    'name': 'description',
    'type': 'STRING'
}, {
    'name':
        'linkedAdAccounts',
    'mode':
        'REPEATED',
    'type':
        'RECORD',
    'fields': [{
        'name': 'kind',
        'type': 'STRING'
    }, {
        'name': 'id',
        'type': 'STRING'
    }, {
        'name': 'accountId',
        'type': 'STRING'
    }, {
        'name': 'webPropertyId',
        'type': 'STRING'
    }, {
        'name': 'internalWebPropertyId',
        'type': 'STRING'
    }, {
        'name': 'remarketingAudienceId',
        'type': 'STRING'
    }, {
        'name': 'linkedAccountId',
        'type': 'STRING'
    }, {
        'name': 'type',
        'type': 'STRING'
    }, {
        'name': 'status',
        'type': 'STRING'
    }, {
        'name': 'eligibleForSearch',
        'type': 'BOOLEAN'
    }]
}, {
    'name': 'linkedViews',
    'type': 'RECORD',
    'mode': 'REPEATED',
    'fields': [{
        'name': 'id',
        'type': 'STRING'
    }]
}, {
    'name': 'audienceType',
    'type': 'STRING'
}, {
    'name':
        'audienceDefinition',
    'type':
        'RECORD',
    'fields': [{
        'name':
            'includeConditions',
        'type':
            'RECORD',
        'fields': [{
            'name': 'kind',
            'type': 'STRING'
        }, {
            'name': 'isSmartList',
            'type': 'BOOLEAN'
        }, {
            'name': 'segment',
            'type': 'STRING'
        }, {
            'name': 'membershipDurationDays',
            'type': 'INTEGER'
        }, {
            'name': 'daysToLookBack',
            'type': 'INTEGER'
        }]
    }]
}, {
    'name':
        'stateBasedAudienceDefinition',
    'type':
        'RECORD',
    'fields': [{
        'name':
            'includeConditions',
        'type':
            'RECORD',
        'fields': [{
            'name': 'kind',
            'type': 'STRING'
        }, {
            'name': 'isSmartList',
            'type': 'BOOLEAN'
        }, {
            'name': 'segment',
            'type': 'STRING'
        }, {
            'name': 'membershipDurationDays',
            'type': 'INTEGER'
        }, {
            'name': 'daysToLookBack',
            'type': 'INTEGER'
        }]
    }, {
        'name':
            'excludeConditions',
        'type':
            'RECORD',
        'fields': [{
            'name': 'segment',
            'type': 'STRING'
        }, {
            'name': 'exclusionDuration',
            'type': 'STRING'
        }]
    }]
}]

ACCOUNT_SUMMARIES_SCHEMA = [{
    'name': 'date',
    'type': 'DATE'
}, {
    'name': 'id',
    'type': 'STRING'
}, {
    'name': 'kind',
    'type': 'STRING'
}, {
    'name': 'name',
    'type': 'STRING'
}, {
    'name': 'starred',
    'type': 'BOOLEAN'
}, {
    'name':
        'webProperties',
    'type':
        'RECORD',
    'mode':
        'REPEATED',
    'fields': [{
        'name': 'kind',
        'type': 'STRING'
    }, {
        'name': 'id',
        'type': 'STRING'
    }, {
        'name': 'name',
        'type': 'STRING'
    }, {
        'name': 'internalWebPropertyId',
        'type': 'STRING'
    }, {
        'name': 'level',
        'type': 'STRING'
    }, {
        'name': 'websiteUrl',
        'type': 'STRING'
    }, {
        'name': 'starred',
        'type': 'BOOLEAN'
    }, {
        'name':
            'profiles',
        'type':
            'RECORD',
        'mode':
            'REPEATED',
        'fields': [
            {
                'name': 'kind',
                'type': 'STRING'
            },
            {
                'name': 'id',
                'type': 'STRING'
            },
            {
                'name': 'name',
                'type': 'STRING'
            },
            {
                'name': 'type',
                'type': 'STRING'
            },
            {
                'name': 'starred',
                'type': 'BOOLEAN'
            },
        ]
    }]
}]
